import json
from decimal import Decimal, InvalidOperation
from rest_framework import serializers
from apps.gestionDeVentasYFacturacion.cu13_gestionar_estado_de_pedido.models.pedido import Pedido
from apps.gestionDeVentasYFacturacion.cu11_gestion_carrito_de_compras.api.carrito_serializers import CarritoItemSerializer


class PedidoSerializer(serializers.ModelSerializer):
    carrito_id = serializers.IntegerField(source='carrito.id', read_only=True)
    cliente_nombre = serializers.CharField(source='carrito.cliente.nombre', read_only=True)
    cliente_email = serializers.CharField(source='carrito.cliente.correo', read_only=True)
    subtotal_pedido = serializers.DecimalField(
        source='carrito.total_carrito',
        max_digits=12,
        decimal_places=2,
        read_only=True
    )
    total_pedido = serializers.SerializerMethodField()
    descuento_puntos = serializers.SerializerMethodField()
    puntos_canjeados = serializers.SerializerMethodField()
    cantidad_items = serializers.IntegerField(source='carrito.cantidad_items', read_only=True)
    items = CarritoItemSerializer(source='carrito.items', many=True, read_only=True)

    def _get_fidelizacion_data(self, obj):
        if not obj.observaciones:
            return {}

        try:
            observaciones = json.loads(obj.observaciones)
        except (TypeError, ValueError):
            return {}

        data = observaciones.get('fidelizacion_checkout') if isinstance(observaciones, dict) else {}
        return data if isinstance(data, dict) else {}

    def get_descuento_puntos(self, obj):
        raw_value = self._get_fidelizacion_data(obj).get('descuento_puntos', 0)
        try:
            return Decimal(str(raw_value or 0)).quantize(Decimal('0.01'))
        except (InvalidOperation, ValueError):
            return Decimal('0.00')

    def get_puntos_canjeados(self, obj):
        raw_value = self._get_fidelizacion_data(obj).get('puntos_canjeados', 0)
        try:
            return max(0, int(float(raw_value or 0)))
        except (TypeError, ValueError):
            return 0

    def get_total_pedido(self, obj):
        subtotal = Decimal(str(obj.carrito.total_carrito or 0))
        total = subtotal - self.get_descuento_puntos(obj)
        return max(total, Decimal('0.00')).quantize(Decimal('0.01'))
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'carrito', 'carrito_id', 'cliente_nombre', 'cliente_email', 'estado',
            'fecha_creacion', 'fecha_actualizacion', 'observaciones',
            'subtotal_pedido', 'descuento_puntos', 'puntos_canjeados',
            'total_pedido', 'cantidad_items', 'items'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
