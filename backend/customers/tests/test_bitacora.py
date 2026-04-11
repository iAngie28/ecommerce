from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from customers.models.bitacora import Bitacora
from customers.services.bitacora_service import BitacoraService
from app_negocio.models.producto import Producto

Usuario = get_user_model()

class BitacoraTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Usuario.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )

    def test_registrar_acceso_captura_ip_y_browser(self):
        """Prueba que registrar_acceso guarde IP y Browser correctamente."""
        request = self.factory.post('/api/login/', HTTP_USER_AGENT='TestBrowser', REMOTE_ADDR='1.2.3.4')
        
        BitacoraService.registrar_acceso(request, self.user, "LOGIN")
        
        log = Bitacora.objects.filter(idUsuario=self.user, accion="LOGIN").first()
        self.assertIsNotNone(log)
        self.assertEqual(log.metadatos['ip'], '1.2.3.4')
        self.assertEqual(log.metadatos['browser'], 'TestBrowser')

    def test_registrar_accion_negocio_guarda_detalles(self):
        """Prueba que las acciones de negocio guarden metadatos específicos."""
        metadatos = {'id_producto': 99, 'nombre': 'Producto Test'}
        BitacoraService.registrar_accion(self.user, "Producto", "CREAR", metadatos=metadatos)
        
        log = Bitacora.objects.filter(idUsuario=self.user, modulo="Producto", accion="CREAR").first()
        self.assertIsNotNone(log)
        self.assertEqual(log.metadatos['id_producto'], 99)
        self.assertEqual(log.metadatos['nombre'], 'Producto Test')

    def test_filtrado_datos_sensibles(self):
        """Prueba que el servicio oculte contraseñas en los metadatos."""
        metadatos = {'email': 'test@example.com', 'password': 'secreto123'}
        BitacoraService.registrar_accion(self.user, "Usuario", "CREAR", metadatos=metadatos)
        
        log = Bitacora.objects.filter(idUsuario=self.user, modulo="Usuario").first()
        self.assertEqual(log.metadatos['password'], "********")
        self.assertEqual(log.metadatos['email'], "test@example.com")
