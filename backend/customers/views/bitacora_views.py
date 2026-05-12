from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from customers.models.bitacora import Bitacora
from customers.serializers.bitacora_serializer import BitacoraSerializer

class BitacoraViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver la bitácora de acciones del sistema. Solo lectura.
    """
    queryset = Bitacora.objects.all()
    serializer_class = BitacoraSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = {
        'accion': ['exact', 'icontains'],
        'modulo': ['exact', 'icontains'],
        'idUsuario': ['exact'],
        'fecha': ['gte', 'lte'],
    }
    search_fields = ['accion', 'modulo', 'idUsuario__email', 'idUsuario__first_name']
    ordering_fields = ['fecha', 'accion']
