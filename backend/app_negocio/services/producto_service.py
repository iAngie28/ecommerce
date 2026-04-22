from core.services import BaseService
from app_negocio.models.producto import Producto

class ProductoService(BaseService):
    def __init__(self):
        super().__init__(Producto)