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
