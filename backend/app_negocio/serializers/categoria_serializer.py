from rest_framework import serializers
from app_negocio.models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    ruta_completa = serializers.CharField(read_only=True)
    
    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'descripcion', 'parent', 
            'activo', 'fecha_creacion', 'ruta_completa'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'ruta_completa']
