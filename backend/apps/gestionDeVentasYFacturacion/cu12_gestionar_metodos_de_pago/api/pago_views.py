import stripe
import json
from django.db import connection
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django_tenants.utils import schema_context
import logging

from apps.gestionDeVentasYFacturacion.cu13_gestionar_estado_de_pedido.models.pedido import Pedido
from apps.gestionDeVentasYFacturacion.cu11_gestion_carrito_de_compras.models.carrito import Carrito
from apps.gestionDeVentasYFacturacion.cu11_gestion_carrito_de_compras.models.carrito_item import CarritoItem
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.services.fidelizacion_service import FidelizacionService

logger = logging.getLogger(__name__)

class PagoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    LOYALTY_OBSERVATION_KEY = 'fidelizacion_checkout'
    ESTADOS_CON_PAGO_CONFIRMADO = {'PAGADO', 'PROCESADO', 'ENVIADO', 'ENTREGADO'}

    def _get_stripe_key(self):
        key = getattr(settings, 'STRIPE_SECRET_KEY', None)
        if not key:
            print("[ERROR] No se encontró STRIPE_SECRET_KEY en settings")
            return None
        stripe.api_key = key
        return key

    def _to_positive_int(self, value):
        try:
            return max(0, int(float(value or 0)))
        except (TypeError, ValueError):
            return 0

    def _read_observaciones(self, pedido):
        if not pedido.observaciones:
            return {}

        try:
            data = json.loads(pedido.observaciones)
        except (TypeError, ValueError):
            return {'nota': pedido.observaciones}

        return data if isinstance(data, dict) else {'nota': str(data)}

    def _guardar_fidelizacion_checkout(self, pedido, loyalty_data):
        observaciones = self._read_observaciones(pedido)
        observaciones[self.LOYALTY_OBSERVATION_KEY] = loyalty_data
        pedido.observaciones = json.dumps(observaciones)

    def _obtener_fidelizacion_checkout(self, pedido, metadata=None):
        data = {}
        observaciones = self._read_observaciones(pedido)
        guardado = observaciones.get(self.LOYALTY_OBSERVATION_KEY)

        if isinstance(guardado, dict):
            data.update(guardado)

        metadata_get = getattr(metadata, 'get', None)
        if metadata_get:
            for key in ('puntos_canjeados', 'descuento_puntos_centavos', 'descuento_puntos', 'referencia'):
                value = metadata_get(key)
                if value not in (None, ''):
                    data[key] = value

        return data

    def _preparar_descuento_puntos(self, request, pedido, subtotal_centavos):
        puntos_canjeados = self._to_positive_int(request.data.get('puntos_canjeados'))
        if puntos_canjeados <= 0:
            loyalty_guardado = FidelizacionService.obtener_canje_pendiente_pedido(pedido)
            puntos_canjeados = self._to_positive_int(loyalty_guardado.get('puntos_canjeados'))

        if puntos_canjeados <= 0:
            return None, None

        if not pedido.carrito_id or not pedido.carrito.cliente_id:
            return None, Response({'error': 'El pedido no tiene un cliente asociado para canjear puntos'}, status=400)

        cuenta = FidelizacionService.obtener_o_crear_cuenta(pedido.carrito.cliente_id)
        if cuenta.saldo_actual < puntos_canjeados:
            return None, Response({
                'error': f'Saldo insuficiente. Tienes {cuenta.saldo_actual} puntos.'
            }, status=400)

        descuento_centavos = int(round(
            puntos_canjeados * FidelizacionService.VALOR_BS_POR_PUNTO * 100
        ))

        if descuento_centavos <= 0:
            return None, Response({'error': 'El descuento por puntos debe ser mayor a 0'}, status=400)

        if descuento_centavos > subtotal_centavos:
            return None, Response({
                'error': 'El descuento por puntos no puede superar el total del carrito'
            }, status=400)

        return {
            'puntos_canjeados': puntos_canjeados,
            'descuento_puntos_centavos': descuento_centavos,
            'descuento_puntos': f'{descuento_centavos / 100:.2f}',
            'referencia': f'Canje Pedido #{pedido.id}',
        }, None

    def _aplicar_canje_puntos_pedido(self, pedido, metadata=None):
        loyalty_data = FidelizacionService.obtener_canje_pendiente_pedido(pedido, metadata)
        puntos_canjeados = self._to_positive_int(loyalty_data.get('puntos_canjeados'))

        if puntos_canjeados <= 0:
            return

        try:
            descuento = FidelizacionService.aplicar_canje_pendiente_pedido(pedido, metadata)
            print(
                f"[POINTS] Canje aplicado para pedido {pedido.id}: "
                f"{puntos_canjeados} pts = Bs. {float(descuento or 0):.2f}"
            )
        except ValidationError as e:
            detalle = e.messages[0] if hasattr(e, 'messages') and e.messages else str(e)
            print(f"[WARN] No se pudo canjear puntos del pedido {pedido.id}: {detalle}")
        except Exception as e:
            print(f"[WARN] Error aplicando canje de puntos del pedido {pedido.id}: {str(e)}")

    def _resolve_schema_name(self, tenant):
        tenant = str(tenant or '').strip()
        if not tenant:
            return None

        if tenant == 'public':
            return 'public'

        try:
            from apps.customers.models import Client, Domain

            client = Client.objects.filter(schema_name=tenant).first()
            if client:
                return client.schema_name

            domain = Domain.objects.filter(domain=tenant).select_related('tenant').first()
            if not domain:
                domain = Domain.objects.filter(domain__startswith=f'{tenant}.').select_related('tenant').first()
            if domain:
                return domain.tenant.schema_name
        except Exception as e:
            print(f"[WARN] No se pudo resolver tenant '{tenant}': {str(e)}")

        return tenant

    @action(detail=False, methods=['post'], url_path='create-payment-intent')
    def create_payment_intent(self, request):
        pedido_id = request.data.get('pedido_id')
        print(f"[PAY] Creando PaymentIntent para pedido: {pedido_id}")
        
        if not self._get_stripe_key():
            return Response({'error': 'Configuración de Stripe incompleta'}, status=500)

        try:
            pedido = Pedido.objects.get(id=pedido_id)
            if pedido.estado == 'PAGADO':
                return Response({'error': 'Este pedido ya ha sido pagado'}, status=400)

            # Calcular monto total
            monto_centavos = 0
            for item in pedido.carrito.items.all():
                if item.producto.precio:
                    monto_centavos += int(round(float(item.producto.precio) * 100 * item.cantidad))

            if monto_centavos == 0:
                return Response({'error': 'El monto del pedido es 0'}, status=400)

            loyalty_data, loyalty_error = self._preparar_descuento_puntos(request, pedido, monto_centavos)
            if loyalty_error:
                return loyalty_error

            metadata = {
                'pedido_id': str(pedido.id),
                'tenant': str(connection.schema_name)
            }
            monto_final_centavos = monto_centavos
            if loyalty_data:
                monto_final_centavos -= loyalty_data['descuento_puntos_centavos']
                metadata.update({
                    'puntos_canjeados': str(loyalty_data['puntos_canjeados']),
                    'descuento_puntos_centavos': str(loyalty_data['descuento_puntos_centavos']),
                    'descuento_puntos': loyalty_data['descuento_puntos'],
                    'referencia': loyalty_data['referencia'],
                })

                FidelizacionService.guardar_canje_pendiente_pedido(
                    pedido,
                    loyalty_data['puntos_canjeados'],
                    loyalty_data,
                )

            if monto_final_centavos <= 0:
                self._marcar_pagado(pedido.id, metadata)
                return Response({
                    'payment_required': False,
                    'mensaje': 'Pedido pagado completamente con puntos.',
                    'amount': 0,
                    'subtotal': monto_centavos,
                    'discount': loyalty_data['descuento_puntos_centavos'] if loyalty_data else 0,
                    'puntos_canjeados': loyalty_data['puntos_canjeados'] if loyalty_data else 0,
                })

            # Crear el PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=monto_final_centavos,
                currency='bob',
                metadata=metadata,
                automatic_payment_methods={
                    'enabled': True,
                },
            )

            pedido.stripe_session_id = intent.id
            if loyalty_data:
                loyalty_data['stripe_payment_intent_id'] = intent.id
                FidelizacionService.guardar_canje_pendiente_pedido(
                    pedido,
                    loyalty_data['puntos_canjeados'],
                    loyalty_data,
                    save=False
                )
            pedido.save()

            return Response({
                'paymentIntent': intent.client_secret,
                'publishableKey': settings.STRIPE_PUBLISHABLE_KEY,
                'payment_required': True,
                'amount': monto_final_centavos,
                'subtotal': monto_centavos,
                'discount': loyalty_data['descuento_puntos_centavos'] if loyalty_data else 0,
                'puntos_canjeados': loyalty_data['puntos_canjeados'] if loyalty_data else 0,
            })

        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=404)
        except Exception as e:
            print(f"[ERROR] Error creando PaymentIntent: {str(e)}")
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['post'], url_path='create-checkout-session')
    def create_checkout_session(self, request):
        pedido_id = request.data.get('pedido_id')
        print(f"[BOX] Procesando pago para pedido: {pedido_id}")
        
        if not self._get_stripe_key():
            return Response({'error': 'Configuración de Stripe incompleta'}, status=500)

        try:
            pedido = Pedido.objects.get(id=pedido_id)
            
            if pedido.estado == 'PAGADO':
                return Response({'error': 'Este pedido ya ha sido pagado'}, status=400)

            # Preparar items
            line_items = []
            subtotal_centavos = 0
            if not hasattr(pedido, 'carrito') or not pedido.carrito:
                print("[ERROR] El pedido no tiene carrito")
                return Response({'error': 'El pedido no tiene un carrito asociado'}, status=400)

            for item in pedido.carrito.items.all():
                if not item.producto.precio:
                    print(f"[WARN] ADVERTENCIA: El producto {item.producto.nombre} no tiene precio.")
                    continue
                monto_centavos = int(round(float(item.producto.precio) * 100))
                cantidad = int(item.cantidad)
                subtotal_centavos += monto_centavos * cantidad
                line_items.append({
                    'price_data': {
                        'currency': 'bob',
                        'product_data': {
                            'name': item.producto.nombre,
                        },
                        'unit_amount': monto_centavos,
                    },
                    'quantity': cantidad,
                })

            if not line_items:
                return Response({'error': 'El carrito está vacío'}, status=400)

            loyalty_data, loyalty_error = self._preparar_descuento_puntos(request, pedido, subtotal_centavos)
            if loyalty_error:
                return loyalty_error

            session_metadata = {
                'pedido_id': str(pedido.id),
                'tenant': str(connection.schema_name)
            }
            session_kwargs = {
                'payment_method_types': ['card'],
                'line_items': line_items,
                'mode': 'payment',
                'success_url': request.data.get('success_url'),
                'cancel_url': request.data.get('cancel_url'),
                'metadata': session_metadata,
            }

            if loyalty_data:
                coupon = stripe.Coupon.create(
                    amount_off=loyalty_data['descuento_puntos_centavos'],
                    currency='bob',
                    duration='once',
                    name=f"Descuento puntos pedido #{pedido.id}",
                    metadata={
                        'pedido_id': str(pedido.id),
                        'tenant': str(connection.schema_name),
                        'puntos_canjeados': str(loyalty_data['puntos_canjeados']),
                    }
                )
                loyalty_data['stripe_coupon_id'] = coupon.id
                session_kwargs['discounts'] = [{'coupon': coupon.id}]
                session_metadata.update({
                    'puntos_canjeados': str(loyalty_data['puntos_canjeados']),
                    'descuento_puntos_centavos': str(loyalty_data['descuento_puntos_centavos']),
                    'descuento_puntos': loyalty_data['descuento_puntos'],
                    'referencia': loyalty_data['referencia'],
                })

            # Crear sesión
            checkout_session = stripe.checkout.Session.create(**session_kwargs)
            
            pedido.stripe_session_id = checkout_session.id
            if loyalty_data:
                loyalty_data['stripe_session_id'] = checkout_session.id
                FidelizacionService.guardar_canje_pendiente_pedido(
                    pedido,
                    loyalty_data['puntos_canjeados'],
                    loyalty_data,
                    save=False
                )
            pedido.save()

            print(f"[OK] Sesión de Stripe creada: {checkout_session.id}")
            return Response({'id': checkout_session.id, 'url': checkout_session.url})

        except Pedido.DoesNotExist:
            print(f"[ERROR] Pedido {pedido_id} no existe")
            return Response({'error': 'Pedido no encontrado'}, status=404)
        except stripe.error.StripeError as e:
            print(f"[ERROR] STRIPE ERROR: {str(e)}")
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            import traceback
            print(f"[ERROR] BACKEND CRITICAL ERROR creando sesión Stripe: {str(e)}")
            print(f"Datos recibidos: {request.data}")
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['post'], url_path='confirm-success', permission_classes=[IsAuthenticated])
    def confirm_success(self, request):
        pedido_id = request.data.get('pedido_id')
        tenant = request.data.get('tenant')
        
        if not pedido_id:
            return Response({'error': 'pedido_id es requerido'}, status=400)

        print(f"[SYNC] Confirmando éxito para pedido {pedido_id} en tenant {tenant or 'actual'}")
        
        try:
            schema_name = self._resolve_schema_name(tenant)
            if schema_name and schema_name != 'public':
                with schema_context(schema_name):
                    self._marcar_pagado(pedido_id)
            else:
                self._marcar_pagado(pedido_id)
            return Response({'status': 'Pedido marcado como pagado'})
        except Exception as e:
            import traceback
            print(f"[ERROR] Error confirmando éxito: {str(e)}")
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['post'], url_path='confirm-payment', permission_classes=[IsAuthenticated])
    def confirm_payment(self, request):
        """Alias para confirm-success utilizado por la app Flutter"""
        return self.confirm_success(request)

    @action(detail=False, methods=['post'], url_path='webhook', permission_classes=[AllowAny])
    def stripe_webhook(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)

        try:
            if endpoint_secret and sig_header:
                event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            else:
                import json
                event = json.loads(payload)
        except Exception as e:
            print(f"[ERROR] WEBHOOK ERROR: {str(e)}")
            return Response({'error': str(e)}, status=400)

        data_object = event.get('data', {}).get('object', {})
        if event.get('type') in ['checkout.session.completed', 'payment_intent.succeeded']:
            metadata = data_object.get('metadata', {})
            pedido_id = metadata.get('pedido_id')
            tenant = metadata.get('tenant')
            
            if pedido_id and tenant:
                schema_name = self._resolve_schema_name(tenant)
                with schema_context(schema_name or tenant):
                    self._marcar_pagado(pedido_id, metadata)

        return Response(status=200)

    def _marcar_pagado(self, pedido_id, metadata=None):
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            if pedido.estado == 'PENDIENTE':
                pedido.estado = 'PAGADO'
                pedido.save()
                
                try:
                    from apps.gestionDeVentasYFacturacion.cu14_generar_facturacion.services.factura_service import FacturaService
                    from apps.gestionDeVentasYFacturacion.cu12_gestionar_metodos_de_pago.models.tipo_pago import TipoPago
                    tp = TipoPago.objects.filter(nombre__iexact='Stripe').first()
                    if not tp:
                        tp = TipoPago.objects.create(nombre='Stripe')
                    FacturaService().crear_factura_desde_pedido(pedido_id, tp.id)
                    print(f"[DOC] Factura generada para pedido {pedido_id}")
                    
                    # Enviar Notificación de Compra Exitosa al Cliente
                    try:
                        from apps.gestionDeReportes.cu18_gestionar_notificaciones.services.notification_service import send_notification
                        send_notification(
                            cliente=pedido.carrito.cliente,
                            titulo="Compra Exitosa",
                            mensaje=f"Tu pago por el pedido #{pedido.id} ha sido procesado exitosamente.",
                            tipo="PAGO"
                        )
                    except Exception as en:
                        print(f"[WARN] Error al enviar notificación de pago al cliente: {str(en)}")
                        
                    # Enviar Notificación de Nueva Venta al Vendedor
                    try:
                        from apps.gestionDeUsuarioySeguridad.cu3_gestion_de_usuario.models.usuario import Usuario
                        from apps.gestionDeReportes.cu18_gestionar_notificaciones.services.notification_service import send_notification
                        
                        # Buscar los administradores/vendedores de este tenant
                        vendedores = Usuario.objects.filter(tenant__schema_name=connection.schema_name)
                        for vendedor in vendedores:
                            send_notification(
                                usuario=vendedor,
                                titulo="Nueva Venta [MONEY]",
                                mensaje=f"{pedido.carrito.cliente.nombre} ha pagado el pedido #{pedido.id}.",
                                tipo="PEDIDO"
                            )
                    except Exception as env:
                        print(f"[WARN] Error al enviar notificación de pago al vendedor: {str(env)}")
                except Exception as ef:
                    print(f"[WARN] Error al generar factura: {str(ef)}")

            if pedido.estado in self.ESTADOS_CON_PAGO_CONFIRMADO:
                self._aplicar_canje_puntos_pedido(pedido, metadata)
        except Exception as e:
            print(f"[ERROR] ERROR en _marcar_pagado: {str(e)}")
