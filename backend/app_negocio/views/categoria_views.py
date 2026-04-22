from core.views import BaseViewSet
from app_negocio.models import Categoria
from app_negocio.serializers.categoria_serializer import CategoriaSerializer
from app_negocio.services.categoria_service import CategoriaService


class CategoriaViewSet(BaseViewSet):
    """
    API de Categorías de Productos.
    
    - GET /api/categorias/ - Listar todos
    - POST /api/categorias/ - Crear nuevo
    - GET /api/categorias/{id}/ - Detalle
    - PUT /api/categorias/{id}/ - Actualizar
    - DELETE /api/categorias/{id}/ - Eliminar
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    modulo_auditoria = "Categoria"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CategoriaService()
