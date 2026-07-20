from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from apps.gestionDeClientes.cu26_gestionar_fidelizacion.models.cuenta_puntos import CuentaPuntos
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.models.historial_puntos import HistorialPuntos
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.api.serializers import CuentaPuntosSerializer, HistorialPuntosSerializer
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.services.fidelizacion_service import FidelizacionService

class FidelizacionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_cliente(self):
        if hasattr(self.request.user, 'roles') and self.request.user.roles.filter(nombre='CLIENTE').exists():
            return getattr(self.request.user, 'cliente', None)
        return None

    def _is_admin(self):
        if hasattr(self.request.user, 'roles'):
            return self.request.user.roles.filter(nombre='ADMIN').exists()
        return False

    @action(detail=False, methods=['get'], url_path='mi-cuenta')
    def mi_cuenta(self, request):
        cliente = self._get_cliente()
        if not cliente:
            return Response({"detail": "Solo los clientes tienen cuenta de puntos."}, status=status.HTTP_403_FORBIDDEN)
            
        cuenta = FidelizacionService.obtener_o_crear_cuenta(cliente.id)
        serializer = CuentaPuntosSerializer(cuenta)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='canjear')
    def canjear(self, request):
        cliente = self._get_cliente()
        if not cliente:
            return Response({"detail": "Solo los clientes pueden canjear puntos."}, status=status.HTTP_403_FORBIDDEN)
            
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
        if not self._is_admin():
            return Response({"detail": "Permiso denegado."}, status=status.HTTP_403_FORBIDDEN)
            
        return Response({
            'PUNTOS_POR_BS': FidelizacionService.PUNTOS_POR_BS,
            'VALOR_BS_POR_PUNTO': FidelizacionService.VALOR_BS_POR_PUNTO
        })
