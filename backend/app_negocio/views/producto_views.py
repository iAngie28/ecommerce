from core.views import BaseViewSet
from ..models.producto import Producto
from ..serializers.producto_serializer import ProductoSerializer

class ProductoViewSet(BaseViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    modulo_auditoria = "Producto"  # Requerido por el AuditoriaMixin