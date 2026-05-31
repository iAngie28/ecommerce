from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.negocio.reportes.api.views import (
    ReporteConfigViewSet, 
    ReporteEstaticoAPIView, 
    ReportBuilderAPIView
)

router = DefaultRouter()
router.register(r'configuraciones', ReporteConfigViewSet, basename='reporte_config')

urlpatterns = [
    path('estatico/<str:tipo>/', ReporteEstaticoAPIView.as_view(), name='reporte_estatico'),
    path('builder/', ReportBuilderAPIView.as_view(), name='reporte_builder'),
    path('', include(router.urls)),
]
