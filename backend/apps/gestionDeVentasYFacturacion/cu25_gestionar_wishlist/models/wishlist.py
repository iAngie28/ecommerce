from django.db import models
from apps.customers.clientes.models.cliente import Cliente


class Wishlist(models.Model):
    """
    Lista de deseos de un cliente.

    Cada cliente tiene exactamente una Wishlist (se crea automáticamente
    en el primer uso). Los productos guardados se gestionan a través de
    WishlistItem.
    """

    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='wishlist',
        verbose_name='Cliente',
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creado en',
    )

    class Meta:
        app_label = 'app_negocio'
        db_table = 'app_negocio_wishlist'
        verbose_name = 'Lista de Deseos'
        verbose_name_plural = 'Listas de Deseos'

    def __str__(self):
        return f"Wishlist de {self.cliente.nombre}"
