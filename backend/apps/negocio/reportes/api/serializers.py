from rest_framework import serializers
from apps.negocio.reportes.models.reporte_config import ReporteConfig

class ReporteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteConfig
        fields = '__all__'
