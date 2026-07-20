from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ValidationError

from apps.core.views import BaseViewSet
from apps.gestionDeProductoYCatalogo.cu24_gestionar_reseñas.models.reseña import Reseña
from apps.gestionDeProductoYCatalogo.cu24_gestionar_reseñas.api.serializers import ReseñaSerializer, ReseñaPublicaSerializer
from apps.gestionDeProductoYCatalogo.cu24_gestionar_reseñas.services.reseña_service import ReseñaService

class ReseñaViewSet(BaseViewSet):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer
    service = ReseñaService()

    def get_permissions(self):
        if self.action == 'por_producto':
            return [AllowAny()]
        return [IsAuthenticated()]

    def _get_cliente(self):
        # Verifica si el usuario logueado es un CLIENTE
        if hasattr(self.request.user, 'roles') and self.request.user.roles.filter(nombre='CLIENTE').exists():
            return getattr(self.request.user, 'cliente', None)
        return None
        
    def _is_admin_or_vendor(self):
        # Verifica si el usuario logueado es ADMIN o VENDEDOR
        if hasattr(self.request.user, 'roles'):
            return self.request.user.roles.filter(nombre__in=['ADMIN', 'VENDEDOR']).exists()
        return False

    def create(self, request, *args, **kwargs):
        cliente = self._get_cliente()
        if not cliente:
            return Response({"detail": "Solo los clientes pueden crear reseñas."}, status=status.HTTP_403_FORBIDDEN)
            
        producto_id = request.data.get('producto')
        calificacion = request.data.get('calificacion')
        comentario = request.data.get('comentario')
        
        if not producto_id or not calificacion:
            return Response({"detail": "El producto y la calificación son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reseña = self.service.crear_reseña(
                cliente_id=cliente.id,
                producto_id=producto_id,
                calificacion=int(calificacion),
                comentario=comentario
            )
            serializer = self.get_serializer(reseña)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='mis-reseñas')
    def mis_reseñas(self, request):
        cliente = self._get_cliente()
        if not cliente:
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)
            
        reseñas = self.queryset.filter(cliente=cliente)
        
        page = self.paginate_queryset(reseñas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(reseñas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'por-producto/(?P<producto_id>\d+)')
    def por_producto(self, request, producto_id=None):
        # Endpoint público para listar reseñas aprobadas de un producto
        reseñas = self.queryset.filter(producto_id=producto_id, estado='APROBADA')
        promedios = self.service.calcular_promedio(producto_id)
        
        page = self.paginate_queryset(reseñas)
        if page is not None:
            serializer = ReseñaPublicaSerializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['estadisticas'] = promedios
            return response
            
        serializer = ReseñaPublicaSerializer(reseñas, many=True)
        return Response({
            'resultados': serializer.data,
            'estadisticas': promedios
        })

    def partial_update(self, request, *args, **kwargs):
        # Solo permite al cliente editar si está en estado PENDIENTE
        reseña = self.get_object()
        cliente = self._get_cliente()
        
        if not cliente or reseña.cliente_id != cliente.id:
            return Response({"detail": "No tienes permiso para editar esta reseña."}, status=status.HTTP_403_FORBIDDEN)
            
        if reseña.estado != 'PENDIENTE':
            return Response({"detail": "No puedes editar una reseña que ya fue aprobada o rechazada."}, status=status.HTTP_400_BAD_REQUEST)
            
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        if not self._is_admin_or_vendor():
            return Response({"detail": "Permiso denegado."}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            reseña = self.service.cambiar_estado(pk, 'APROBADA', request.user)
            serializer = self.get_serializer(reseña)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"detail": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        if not self._is_admin_or_vendor():
            return Response({"detail": "Permiso denegado."}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            reseña = self.service.cambiar_estado(pk, 'RECHAZADA', request.user)
            serializer = self.get_serializer(reseña)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"detail": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # Solo para administradores/vendedores: Ver todas las reseñas para moderación
        if not self._is_admin_or_vendor():
            return Response({"detail": "Permiso denegado."}, status=status.HTTP_403_FORBIDDEN)
            
        estado = request.query_params.get('estado')
        producto = request.query_params.get('producto')
        cliente = request.query_params.get('cliente')
        
        queryset = self.queryset
        if estado:
            queryset = queryset.filter(estado=estado)
        if producto:
            queryset = queryset.filter(producto_id=producto)
        if cliente:
            queryset = queryset.filter(cliente_id=cliente)
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
