from django.db import models
from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist import Wishlist
from apps.gestionDeProductoYCatalogo.cu7_gestionar_productos.models.producto import Producto


class WishlistItem(models.Model):
    """
    Producto guardado dentro de una Wishlist.

    Restricción unique_together garantiza que el mismo producto no pueda
    aparecer más de una vez en la misma lista de deseos.
    El campo 'notificado' evita enviar múltiples alertas de bajada de precio
    para la misma promoción.
    """

    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Lista de Deseos',
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='en_wishlists',
        verbose_name='Producto',
    )
    agregado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Agregado en',
    )
    notificado = models.BooleanField(
        default=False,
        verbose_name='Notificado por oferta',
        help_text='True si ya se envió una notificación de bajada de precio para este item.',
    )

    class Meta:
        app_label = 'cu25_gestionar_wishlist'
        db_table = 'app_negocio_wishlist_item'
        verbose_name = 'Item de Lista de Deseos'
        verbose_name_plural = 'Items de Wishlist'
        unique_together = [('wishlist', 'producto')]
        ordering = ['-agregado_en']

    def __str__(self):
        return f"{self.producto.nombre} en {self.wishlist}"
