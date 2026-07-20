from rest_framework import serializers
from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist import Wishlist
from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist_item import WishlistItem
from apps.gestionDeProductoYCatalogo.cu7_gestionar_productos.api.serializers import ProductoSerializer


class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializa un item de la wishlist con el detalle completo del producto."""

    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WishlistItem
        fields = [
            'id',
            'producto',
            'producto_id',
            'agregado_en',
            'notificado',
        ]
        read_only_fields = ['id', 'agregado_en', 'notificado']


class WishlistSerializer(serializers.ModelSerializer):
    """Serializa la wishlist completa con sus items."""

    items = WishlistItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = [
            'id',
            'creado_en',
            'total_items',
            'items',
        ]
        read_only_fields = ['id', 'creado_en']

    def get_total_items(self, obj):
        return obj.items.count()
