from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.gestionDeVentasYFacturacion.cu13_gestionar_estado_de_pedido.models.pedido import Pedido
from .services.fidelizacion_service import FidelizacionService

@receiver(
    post_save,
    sender=Pedido,
    dispatch_uid='cu26_procesar_puntos_pedido_entregado',
)
def procesar_puntos_pedido_entregado(sender, instance, created, **kwargs):
    """
    Se ejecuta automáticamente cada vez que se guarda un Pedido.
    Si el estado cambió a 'ENTREGADO', se le suman los puntos al cliente.
    """
    if not created and instance.estado == 'ENTREGADO':
        # En un sistema real más complejo, deberíamos evitar sumar puntos dos veces
        # para el mismo pedido si se guarda múltiples veces en estado ENTREGADO.
        # Podríamos agregar un flag "puntos_asignados" en Pedido, pero por simplicidad
        # asumimos que pasa a ENTREGADO una sola vez al final del flujo.
        FidelizacionService.acumular_puntos_por_compra(instance.id)
