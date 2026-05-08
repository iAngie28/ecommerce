from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from core.views import BaseViewSet
from ..models.producto import Producto
from ..serializers.producto_serializer import ProductoSerializer

class ProductoViewSet(BaseViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    modulo_auditoria = "Producto"  # Requerido por el AuditoriaMixin
    
    def get_permissions(self):
        """
        Permite lectura pública (AllowAny para GET)
        Pero requiere autenticación para crear/editar/eliminar
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]