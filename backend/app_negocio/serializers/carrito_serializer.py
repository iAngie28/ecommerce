from rest_framework import serializers
from app_negocio.models import Carrito, CarritoItem, Producto


class CarritoItemSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_precio = serializers.DecimalField(
        source='producto.precio', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    subtotal = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    
    class Meta:
        model = CarritoItem
        fields = [
            'id', 'producto', 'producto_nombre', 'producto_precio',
            'cantidad', 'fecha_agregado', 'subtotal'
        ]
        read_only_fields = ['id', 'fecha_agregado']


class CarritoSerializer(serializers.ModelSerializer):
    items = CarritoItemSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cantidad_items = serializers.IntegerField(read_only=True)
    total_carrito = serializers.DecimalField(
        read_only=True, 
        max_digits=12, 
        decimal_places=2
    )
    
    class Meta:
        model = Carrito
        fields = [
            'id', 'cliente', 'cliente_nombre', 'estado',
            'fecha_creacion', 'fecha_actualizacion', 
            'items', 'cantidad_items', 'total_carrito'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
