from rest_framework import serializers
from customers.models.bitacora import Bitacora

class BitacoraSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Bitacora
        fields = ['id', 'usuario_nombre', 'fecha', 'accion', 'modulo', 'metadatos']

    def get_usuario_nombre(self, obj):
        try:
            return str(obj.idUsuario.get_full_name() or obj.idUsuario.username)
        except:
            return "Desconocido"