from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.producto import Producto
from ..serializers.producto_serializar import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    """
    Vista de productos multi-tenant.
    
    Cuando la petición llega desde un subdominio (empresa1.localhost),
    el TenantMainMiddleware de django-tenants ya configura el schema correcto
    automáticamente — no necesitamos hacer nada extra.
    
    Cuando la petición llega desde localhost (sin subdominio), el schema
    está en 'public' y no hay tabla de productos, devolvemos lista vacía.
    """
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from django.db import connection
        
        # Si el schema activo es 'public', no hay productos de negocio
        current_schema = connection.schema_name
        if current_schema == 'public':
            return Producto.objects.none()
        
        # El TenantMainMiddleware ya configuró el schema correcto por subdominio
        return Producto.objects.all()