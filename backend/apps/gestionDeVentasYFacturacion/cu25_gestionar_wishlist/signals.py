from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='cu7_gestionar_productos.Promocion')
def notificar_wishlist_en_promocion(sender, instance, **kwargs):
    """
    Cuando una Promocion se guarda (creación o actualización), verifica si está
    vigente y, de ser así, notifica a los clientes que tienen los productos
    de esa promoción en su lista de deseos.

    El campo WishlistItem.notificado evita enviar la misma alerta más de una vez.
    """
    try:
        if not instance.vigente:
            return

        from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist_item import WishlistItem
        from apps.gestionDeReportes.cu18_gestionar_notificaciones.services.notification_service import send_notification

        # Productos que pertenecen a esta promoción
        productos = instance.productos.filter(activo=True)

        for producto in productos:
            items_pendientes = WishlistItem.objects.filter(
                producto=producto,
                notificado=False,
            ).select_related('wishlist__cliente')

            for item in items_pendientes:
                cliente = item.wishlist.cliente
                try:
                    send_notification(
                        cliente=cliente,
                        titulo="¡Oferta en tu lista de deseos!",
                        mensaje=(
                            f"El producto '{producto.nombre}' que guardaste "
                            f"tiene un {instance.descuento_pct}% de descuento. "
                            f"¡Válido hasta el {instance.fecha_fin}!"
                        ),
                        tipo='SISTEMA',
                    )
                    item.notificado = True
                    item.save(update_fields=['notificado'])
                except Exception as e:
                    print(f"[Wishlist Signal] Error al notificar cliente {cliente.id}: {e}")

    except Exception as e:
        print(f"[Wishlist Signal] Error general en notificar_wishlist_en_promocion: {e}")

from django.db.models.signals import pre_save

@receiver(pre_save, sender='cu7_gestionar_productos.Producto')
def check_price_drop(sender, instance, **kwargs):
    """Detecta si el precio del producto ha bajado antes de guardar."""
    if instance.pk:
        try:
            old_product = sender.objects.get(pk=instance.pk)
            if instance.precio < old_product.precio:
                instance._price_dropped = True
                instance._old_precio = old_product.precio
            else:
                instance._price_dropped = False
        except sender.DoesNotExist:
            instance._price_dropped = False
    else:
        instance._price_dropped = False

@receiver(post_save, sender='cu7_gestionar_productos.Producto')
def notificar_wishlist_en_baja_precio(sender, instance, **kwargs):
    """Si el precio bajó, notifica a los clientes que lo tienen en wishlist."""
    if getattr(instance, '_price_dropped', False):
        try:
            from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist_item import WishlistItem
            from apps.gestionDeReportes.cu18_gestionar_notificaciones.services.notification_service import send_notification
            
            items = WishlistItem.objects.filter(producto=instance).select_related('wishlist__cliente')
            for item in items:
                try:
                    send_notification(
                        cliente=item.wishlist.cliente,
                        titulo="¡Bajó de precio!",
                        mensaje=f"El producto '{instance.nombre}' en tu lista de deseos bajó de Bs. {instance._old_precio} a Bs. {instance.precio}. ¡Aprovecha ahora!",
                        tipo='SISTEMA'
                    )
                except Exception as e:
                    print(f"[Wishlist Signal] Error al notificar baja de precio al cliente {item.wishlist.cliente.id}: {e}")
        except Exception as e:
            print(f"[Wishlist Signal] Error general en notificar_wishlist_en_baja_precio: {e}")
