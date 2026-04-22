from rest_framework import serializers
from app_negocio.models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    carrito_id = serializers.IntegerField(source='carrito.id', read_only=True)
    cliente_nombre = serializers.CharField(source='carrito.cliente.nombre', read_only=True)
    total_pedido = serializers.DecimalField(
        source='carrito.total_carrito',
        max_digits=12,
        decimal_places=2,
        read_only=True
    )
    cantidad_items = serializers.IntegerField(source='carrito.cantidad_items', read_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'carrito', 'carrito_id', 'cliente_nombre', 'estado',
            'fecha_creacion', 'fecha_actualizacion', 'observaciones',
            'total_pedido', 'cantidad_items'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
