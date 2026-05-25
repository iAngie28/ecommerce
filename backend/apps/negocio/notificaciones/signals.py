from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.negocio.ordenes.models.pedido import Pedido
from apps.negocio.notificaciones.services.notification_service import send_notification

@receiver(pre_save, sender=Pedido)
def capture_previous_estado(sender, instance, **kwargs):
    if instance.id:
        try:
            old_instance = Pedido.objects.get(id=instance.id)
            instance._old_estado = old_instance.estado
        except Pedido.DoesNotExist:
            instance._old_estado = None
    else:
        instance._old_estado = None

@receiver(post_save, sender=Pedido)
def notify_on_estado_change(sender, instance, created, **kwargs):
    if not created and hasattr(instance, '_old_estado'):
        old_estado = instance._old_estado
        new_estado = instance.estado
        
        if old_estado != new_estado and new_estado in ['ENVIADO', 'ENTREGADO']:
            cliente = instance.carrito.cliente
            mensaje = f"Tu pedido #{instance.id} ahora está: {new_estado}."
            if new_estado == 'ENVIADO':
                titulo = "Pedido en camino 🚚"
            else:
                titulo = "Pedido entregado ✅"
                
            try:
                send_notification(
                    cliente=cliente,
                    titulo=titulo,
                    mensaje=mensaje,
                    tipo='PEDIDO'
                )
            except Exception as e:
                print(f"⚠️ Error al enviar notificación de cambio de estado: {e}")
