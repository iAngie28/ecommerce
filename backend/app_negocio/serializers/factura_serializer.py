from rest_framework import serializers
from app_negocio.models import Factura, TipoPago, DetalleFactura


class TipoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = ['id', 'nombre', 'descripcion', 'estado']
        read_only_fields = ['id']


class DetalleFacturaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = DetalleFactura
        fields = [
            'id', 'producto', 'producto_nombre', 'cantidad',
            'precio_unitario', 'total'
        ]
        read_only_fields = ['id', 'total']


class FacturaSerializer(serializers.ModelSerializer):
    detalles = DetalleFacturaSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_correo = serializers.CharField(source='cliente.correo', read_only=True)
    tipo_pago_nombre = serializers.CharField(source='tipo_pago.nombre', read_only=True, allow_null=True)
    
    class Meta:
        model = Factura
        fields = [
            'nro', 'fecha', 'hora', 'pedido', 'cliente', 'cliente_nombre',
            'cliente_correo', 'tipo_pago', 'tipo_pago_nombre', 'monto_total',
            'moneda', 'cuf', 'estado', 'detalles'
        ]
        read_only_fields = ['nro', 'fecha', 'hora']
