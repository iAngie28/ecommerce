from rest_framework import serializers
from apps.negocio.notificaciones.models.notificacion import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'titulo', 'mensaje', 'tipo', 'leido', 'fecha_creacion']
        read_only_fields = ['id', 'titulo', 'mensaje', 'tipo', 'fecha_creacion']
