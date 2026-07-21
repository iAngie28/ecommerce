from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.db import connection
from django_tenants.utils import schema_context

from apps.customers.models import Cliente, Client
from apps.gestionDeUsuarioySeguridad.cu1_iniciar_sesion.authentication import (
    ClienteJWTAuthentication,
    UsuarioJWTAuthentication,
)
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.models.cuenta_puntos import CuentaPuntos
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.models.historial_puntos import HistorialPuntos
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.api.serializers import CuentaPuntosSerializer, HistorialPuntosSerializer
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.services.fidelizacion_service import FidelizacionService

class FidelizacionViewSet(viewsets.ViewSet):
    authentication_classes = [ClienteJWTAuthentication, UsuarioJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def _get_cliente(self):
        user = self.request.user

        if getattr(user, 'role', None) == 'CLIENTE':
            cliente_id = getattr(user, 'cliente_id', None) or getattr(user, 'id', None)
            return Cliente.objects.filter(id=cliente_id).first()

        if hasattr(user, 'roles') and user.roles.filter(nombre='CLIENTE').exists():
            return getattr(user, 'cliente', None)

        return None

    def _is_admin(self):
        user = self.request.user
        if hasattr(user, 'roles'):
            return user.roles.filter(nombre='ADMIN').exists()
        return False

    def _is_public_schema(self):
        return getattr(connection, 'schema_name', 'public') == 'public'

    def _get_active_tenants(self):
        return Client.objects.filter(activo=True).exclude(schema_name='public')

    def _build_global_cuenta_response(self, cliente):
        saldo_actual = 0
        puntos_historicos = 0
        historial = []
        fecha_actualizacion = None

        for tenant in self._get_active_tenants():
            try:
                with schema_context(tenant.schema_name):
                    FidelizacionService.sincronizar_pedidos_entregados(cliente.id)
                    cuenta = CuentaPuntos.objects.filter(cliente_id=cliente.id).first()
                    if not cuenta:
                        continue

                    saldo_actual += cuenta.saldo_actual
                    puntos_historicos += cuenta.puntos_historicos

                    if cuenta.fecha_actualizacion and (
                        not fecha_actualizacion or cuenta.fecha_actualizacion > fecha_actualizacion
                    ):
                        fecha_actualizacion = cuenta.fecha_actualizacion

                    for movimiento in cuenta.historial.all()[:10]:
                        historial.append({
                            'id': f'{tenant.schema_name}-{movimiento.id}',
                            'tipo_operacion': movimiento.tipo_operacion,
                            'monto_puntos': movimiento.monto_puntos,
                            'referencia': f"{tenant.name}: {movimiento.referencia or 'Movimiento de puntos'}",
                            'fecha': movimiento.fecha,
                        })
            except Exception:
                continue

        historial.sort(key=lambda movimiento: movimiento.get('fecha'), reverse=True)

        return {
            'id': None,
            'cliente_nombre': cliente.nombre,
            'saldo_actual': saldo_actual,
            'puntos_historicos': puntos_historicos,
            'fecha_actualizacion': fecha_actualizacion,
            'historial': historial[:10],
        }

    @action(detail=False, methods=['get'], url_path='mi-cuenta')
    def mi_cuenta(self, request):
        cliente = self._get_cliente()
        if not cliente:
            return Response({"detail": "Solo los clientes tienen cuenta de puntos."}, status=status.HTTP_403_FORBIDDEN)

        if self._is_public_schema():
            return Response(self._build_global_cuenta_response(cliente))

        cuenta = FidelizacionService.obtener_o_crear_cuenta(cliente.id)
        serializer = CuentaPuntosSerializer(cuenta)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='canjear')
    def canjear(self, request):
        cliente = self._get_cliente()
        if not cliente:
            return Response({"detail": "Solo los clientes pueden canjear puntos."}, status=status.HTTP_403_FORBIDDEN)

        if self._is_public_schema():
            return Response(
                {"detail": "El canje de puntos debe realizarse desde una tienda específica."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        puntos_a_canjear = request.data.get('puntos')
        referencia = request.data.get('referencia', 'Canje desde la App')
        
        if not puntos_a_canjear:
            return Response({"detail": "Debe especificar los puntos a canjear."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            descuento_bs = FidelizacionService.canjear_puntos(
                cliente_id=cliente.id, 
                puntos_a_canjear=int(puntos_a_canjear), 
                referencia=referencia
            )
            
            # Retorna la cuenta actualizada y el descuento obtenido
            cuenta = FidelizacionService.obtener_o_crear_cuenta(cliente.id)
            return Response({
                'mensaje': 'Canje exitoso',
                'descuento_bs': descuento_bs,
                'cuenta': CuentaPuntosSerializer(cuenta).data
            })
        except ValueError:
            return Response({"detail": "Formato de puntos inválido."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

    # ── ENDPOINTS ADMINISTRATIVOS ──

    @action(detail=False, methods=['get'], url_path='clientes')
    def listar_cuentas(self, request):
        if not self._is_admin():
            return Response({"detail": "Permiso denegado."}, status=status.HTTP_403_FORBIDDEN)
            
        cuentas = CuentaPuntos.objects.all()
        serializer = CuentaPuntosSerializer(cuentas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='configuracion')
    def ver_configuracion(self, request):
        return Response({
            'PUNTOS_POR_BS': FidelizacionService.PUNTOS_POR_BS,
            'VALOR_BS_POR_PUNTO': FidelizacionService.VALOR_BS_POR_PUNTO
        })
