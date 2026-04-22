from core.views import BaseViewSet
from customers.models import Cliente
from customers.serializers.cliente_serializer import ClienteSerializer
from customers.services.cliente_service import ClienteService


class ClienteViewSet(BaseViewSet):
    """
    API de Clientes (Customers).
    
    - GET /api/clientes/ - Listar todos
    - POST /api/clientes/ - Crear nuevo
    - GET /api/clientes/{id}/ - Detalle
    - PUT /api/clientes/{id}/ - Actualizar
    - DELETE /api/clientes/{id}/ - Eliminar
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    modulo_auditoria = "Cliente"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ClienteService()
