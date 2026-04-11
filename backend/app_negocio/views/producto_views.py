from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.producto import Producto
from ..serializers.producto_serializar import ProductoSerializer
from customers.services.bitacora_service import BitacoraService


class ProductoViewSet(viewsets.ModelViewSet):
    """
    Vista de productos multi-tenant con auditoría.
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

    def perform_create(self, serializer):
        producto = serializer.save()
        BitacoraService.registrar_accion(
            self.request.user, "Producto", "CREAR",
            request=self.request,
            metadatos={
                'id_producto': producto.id,
                'nombre': producto.nombre,
                'precio': str(producto.precio)
            }
        )

    def perform_update(self, serializer):
        producto = serializer.save()
        BitacoraService.registrar_accion(
            self.request.user, "Producto", "EDITAR",
            request=self.request,
            metadatos={
                'id_producto': producto.id,
                'nombre': producto.nombre,
                'cambios': serializer.initial_data 
            }
        )

    def perform_destroy(self, instance):
        id_producto = instance.id
        nombre_producto = instance.nombre
        instance.delete()
        BitacoraService.registrar_accion(
            self.request.user, "Producto", "ELIMINAR",
            request=self.request,
            metadatos={
                'id_producto': id_producto,
                'nombre': nombre_producto
            }
        )