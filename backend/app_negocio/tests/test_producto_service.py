from django_tenants.test.cases import TenantTestCase
from app_negocio.services.producto_service import ProductoService
from app_negocio.models.producto import Producto

class ProductoServiceTest(TenantTestCase):
    def setUp(self):
        # CRÍTICO: Esto crea un tenant y un dominio "falso" automáticamente para la prueba
        super().setUp() 
        self.service = ProductoService()

    