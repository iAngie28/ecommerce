from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.views import BaseViewSet
from app_negocio.models import Carrito
from app_negocio.serializers.carrito_serializer import CarritoSerializer
from app_negocio.services.carrito_service import CarritoService


class CarritoViewSet(BaseViewSet):
    """
    API de Carritos de Compra.
    
    - GET /api/carritos/ - Listar todos
    - POST /api/carritos/ - Crear nuevo
    - GET /api/carritos/{id}/ - Detalle con items
    - PUT /api/carritos/{id}/ - Actualizar estado
    - DELETE /api/carritos/{id}/ - Eliminar
    
    Acciones especiales:
    - POST /api/carritos/{id}/agregar-item/ - Agregar producto al carrito
    - POST /api/carritos/{id}/eliminar-item/ - Remover producto
    - POST /api/carritos/{id}/vaciar/ - Limpiar todos los items
    - POST /api/carritos/{id}/cerrar/ - Convertir en pedido
    """
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    modulo_auditoria = "Carrito"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CarritoService()
    
    @action(detail=True, methods=['post'])
    def agregar_item(self, request, pk=None):
        """Agrega un producto al carrito."""
        try:
            carrito = self.get_object()
            producto_id = request.data.get('producto_id')
            cantidad = request.data.get('cantidad', 1)
            
            self.service.agregar_item(carrito.id, producto_id, cantidad)
            carrito.refresh_from_db()
            serializer = self.get_serializer(carrito)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def eliminar_item(self, request, pk=None):
        """Elimina un producto del carrito."""
        try:
            carrito = self.get_object()
            producto_id = request.data.get('producto_id')
            
            self.service.eliminar_item(carrito.id, producto_id)
            carrito.refresh_from_db()
            serializer = self.get_serializer(carrito)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def vaciar(self, request, pk=None):
        """Vacía todos los items del carrito."""
        carrito = self.get_object()
        self.service.vaciar_carrito(carrito.id)
        carrito.refresh_from_db()
        serializer = self.get_serializer(carrito)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        """Cierra el carrito para convertirlo en pedido."""
        carrito = self.get_object()
        self.service.cerrar_carrito(carrito.id)
        carrito.refresh_from_db()
        serializer = self.get_serializer(carrito)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
