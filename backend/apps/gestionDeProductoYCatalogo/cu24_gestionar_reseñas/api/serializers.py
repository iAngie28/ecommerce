from rest_framework import serializers
from apps.gestionDeProductoYCatalogo.cu24_gestionar_reseñas.models.reseña import Reseña

class ReseñaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Reseña
        fields = ['id', 'producto', 'cliente', 'cliente_nombre', 'calificacion', 'comentario', 'estado', 'fecha_creacion']
        read_only_fields = ['id', 'cliente', 'estado', 'fecha_creacion', 'cliente_nombre']

    def get_cliente_nombre(self, obj):
        try:
            return obj.cliente.usuario.get_full_name() or obj.cliente.usuario.username
        except Exception:
            return "Usuario Desconocido"

class ReseñaPublicaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Reseña
        fields = ['id', 'cliente_nombre', 'calificacion', 'comentario', 'fecha_creacion']
        read_only_fields = fields
        
    def get_cliente_nombre(self, obj):
        try:
            return obj.cliente.usuario.get_full_name() or obj.cliente.usuario.username
        except Exception:
            return "Usuario Desconocido"
