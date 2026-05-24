from django_tenants.test.cases import TenantTestCase
from apps.negocio.catalogo.services.producto_service import ProductoService
from apps.negocio.catalogo.models.producto import Producto

class ProductoServiceTest(TenantTestCase):
    def setUp(self):
        # CRÍTICO: Esto crea un tenant y un dominio "falso" automáticamente para la prueba
        super().setUp() 
        self.service = ProductoService()

    