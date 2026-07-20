from rest_framework import serializers
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.models.cuenta_puntos import CuentaPuntos
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.models.historial_puntos import HistorialPuntos

class HistorialPuntosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPuntos
        fields = ['id', 'tipo_operacion', 'monto_puntos', 'referencia', 'fecha']

class CuentaPuntosSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.SerializerMethodField()
    historial = serializers.SerializerMethodField()

    class Meta:
        model = CuentaPuntos
        fields = ['id', 'cliente_nombre', 'saldo_actual', 'puntos_historicos', 'fecha_actualizacion', 'historial']

    def get_cliente_nombre(self, obj):
        try:
            return obj.cliente.usuario.get_full_name() or obj.cliente.usuario.username
        except Exception:
            return "Cliente Desconocido"

    def get_historial(self, obj):
        # Retorna solo los últimos 10 movimientos para no sobrecargar
        movimientos = obj.historial.all()[:10]
        return HistorialPuntosSerializer(movimientos, many=True).data
