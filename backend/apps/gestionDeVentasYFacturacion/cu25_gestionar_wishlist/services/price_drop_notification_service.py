def notificar_baja_precio_producto(producto, precio_anterior, precio_nuevo=None):
    """
    Notifica a los clientes que tienen el producto en wishlist cuando baja el precio.

    Reinicia WishlistItem.notificado para permitir una nueva ronda de notificacion
    por cada nueva bajada real de precio.
    """
    from apps.gestionDeReportes.cu18_gestionar_notificaciones.services.notification_service import send_notification
    from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist_item import WishlistItem

    precio_actual = precio_nuevo if precio_nuevo is not None else producto.precio

    WishlistItem.objects.filter(producto=producto).update(notificado=False)
    items_pendientes = WishlistItem.objects.filter(
        producto=producto,
        notificado=False,
    ).select_related('wishlist__cliente')

    total = 0
    for item in items_pendientes:
        cliente = item.wishlist.cliente
        try:
            send_notification(
                cliente=cliente,
                titulo="¡Bajó de precio!",
                mensaje=(
                    f"El producto '{producto.nombre}' en tu lista de deseos "
                    f"bajó de Bs. {precio_anterior} a Bs. {precio_actual}. "
                    "¡Aprovecha ahora!"
                ),
                tipo='SISTEMA',
            )
            item.notificado = True
            item.save(update_fields=['notificado'])
            total += 1
        except Exception as e:
            print(
                "[Wishlist Price Drop] Error al notificar baja de precio "
                f"al cliente {cliente.id}: {e}"
            )

    return total
