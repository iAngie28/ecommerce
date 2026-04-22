from core.views import BaseViewSet
from customers.models import Rol
from customers.serializers.rol_serializer import RolSerializer
from customers.services.rol_service import RolService


class RolViewSet(BaseViewSet):
    """
    API de Roles.
    
    - GET /api/roles/ - Listar todos
    - POST /api/roles/ - Crear nuevo
    - GET /api/roles/{id}/ - Detalle
    - PUT /api/roles/{id}/ - Actualizar
    - DELETE /api/roles/{id}/ - Eliminar
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    modulo_auditoria = "Rol"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = RolService()
