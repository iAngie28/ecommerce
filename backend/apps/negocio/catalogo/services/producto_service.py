from apps.core.services import BaseService
from apps.negocio.catalogo.models.producto import Producto

class ProductoService(BaseService):
    def __init__(self):
        super().__init__(Producto)