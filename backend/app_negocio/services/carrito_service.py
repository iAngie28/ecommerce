from core.services import BaseService
from app_negocio.models import Carrito, CarritoItem, Producto
from django.db import transaction


class CarritoService(BaseService):
    """Servicio de Carritos de Compra."""
    
    def __init__(self):
        super().__init__(Carrito)
    
    def obtener_carrito_abierto(self, cliente_id):
        """Obtiene el carrito abierto de un cliente (o lo crea)."""
        from customers.models import Cliente
        cliente = Cliente.objects.get(id=cliente_id)
        carrito, _ = Carrito.objects.get_or_create(
            cliente=cliente,
            estado='ABIERTO'
        )
        return carrito
    
    @transaction.atomic
    def agregar_item(self, carrito_id, producto_id, cantidad=1):
        """Agrega un producto al carrito."""
        carrito = self.obtener(carrito_id)
        producto = Producto.objects.get(id=producto_id)
        
        # Validar stock disponible
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}")
        
        # Agregar o actualizar item
        item, created = CarritoItem.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        
        if not created:
            item.cantidad += cantidad
            item.save()
        
        return item
    
    @transaction.atomic
    def eliminar_item(self, carrito_id, producto_id):
        """Elimina un producto del carrito."""
        CarritoItem.objects.filter(
            carrito_id=carrito_id,
            producto_id=producto_id
        ).delete()
    
    def vaciar_carrito(self, carrito_id):
        """Vacía todos los items del carrito."""
        CarritoItem.objects.filter(carrito_id=carrito_id).delete()
    
    @transaction.atomic
    def cerrar_carrito(self, carrito_id):
        """Cierra un carrito para convertirlo en pedido."""
        carrito = self.obtener(carrito_id)
        carrito.estado = 'CERRADO'
        carrito.save()
        return carrito
