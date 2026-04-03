from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.producto import Producto
from ..serializers.producto_serializar import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]