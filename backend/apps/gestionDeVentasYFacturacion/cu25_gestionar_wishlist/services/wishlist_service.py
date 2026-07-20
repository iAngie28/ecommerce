from django.db import transaction
from apps.core.services import BaseService
from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist import Wishlist
from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist_item import WishlistItem
from apps.gestionDeProductoYCatalogo.cu7_gestionar_productos.models.producto import Producto


class WishlistService(BaseService):
    """
    Servicio de Lista de Deseos (Wishlist).

    Centraliza toda la lógica de negocio: obtener/crear wishlist,
    agregar/eliminar productos, toggle, mover al carrito y vaciar.
    """

    def __init__(self):
        super().__init__(Wishlist)

    # ------------------------------------------------------------------
    # Obtener / Crear
    # ------------------------------------------------------------------

    def obtener_o_crear(self, cliente_id) -> Wishlist:
        """
        Retorna la Wishlist del cliente, creándola si todavía no existe.
        Acepta tanto la instancia de Cliente como el ID entero.
        """
        from apps.customers.clientes.models.cliente import Cliente
        cliente = Cliente.objects.get(id=cliente_id)
        wishlist, _ = Wishlist.objects.get_or_create(cliente=cliente)
        return wishlist

    # ------------------------------------------------------------------
    # Agregar / Eliminar
    # ------------------------------------------------------------------

    @transaction.atomic
    def agregar_producto(self, cliente_id, producto_id) -> WishlistItem:
        """
        Agrega un producto activo a la wishlist del cliente.

        - Si el producto ya estaba, retorna el item existente (idempotente).
        - Lanza ValueError si el producto no existe o está inactivo.
        """
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            raise ValueError(f"El producto con id={producto_id} no existe.")

        if not producto.activo:
            raise ValueError("No se pueden agregar productos inactivos a la lista de deseos.")

        wishlist = self.obtener_o_crear(cliente_id)
        item, _ = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            producto=producto,
        )
        return item

    @transaction.atomic
    def eliminar_producto(self, cliente_id, producto_id) -> None:
        """
        Elimina un producto de la wishlist del cliente.
        Lanza ValueError si el item no existe.
        """
        wishlist = self.obtener_o_crear(cliente_id)
        deleted, _ = WishlistItem.objects.filter(
            wishlist=wishlist,
            producto_id=producto_id,
        ).delete()
        if not deleted:
            raise ValueError("El producto no se encuentra en tu lista de deseos.")

    @transaction.atomic
    def toggle_producto(self, cliente_id, producto_id) -> dict:
        """
        Agrega el producto si no está en la wishlist; lo elimina si ya está.

        Retorna:
            {'accion': 'agregado'}  o  {'accion': 'eliminado'}
        """
        wishlist = self.obtener_o_crear(cliente_id)
        existe = WishlistItem.objects.filter(
            wishlist=wishlist,
            producto_id=producto_id,
        ).exists()

        if existe:
            self.eliminar_producto(cliente_id, producto_id)
            return {'accion': 'eliminado'}
        else:
            self.agregar_producto(cliente_id, producto_id)
            return {'accion': 'agregado'}

    # ------------------------------------------------------------------
    # Mover al carrito
    # ------------------------------------------------------------------

    @transaction.atomic
    def mover_al_carrito(self, cliente_id, producto_id) -> None:
        """
        Agrega el producto al carrito activo del cliente y lo elimina de la
        wishlist. Si el stock es insuficiente lanza ValueError.
        """
        from apps.gestionDeVentasYFacturacion.cu11_gestion_carrito_de_compras.services.carrito_service import CarritoService

        # Validar stock antes de cualquier cambio
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            raise ValueError(f"El producto con id={producto_id} no existe.")

        if producto.stock <= 0:
            raise ValueError(
                f"Sin stock disponible para '{producto.nombre}'. "
                "El producto permanece en tu lista de deseos."
            )

        carrito_service = CarritoService()
        carrito = carrito_service.obtener_carrito_abierto(cliente_id)
        carrito_service.agregar_item(carrito.id, producto_id, cantidad=1)

        # Solo eliminar de la wishlist si el carrito se actualizó con éxito
        self.eliminar_producto(cliente_id, producto_id)

    # ------------------------------------------------------------------
    # Vaciar
    # ------------------------------------------------------------------

    @transaction.atomic
    def vaciar(self, cliente_id) -> int:
        """
        Elimina todos los WishlistItems del cliente.
        Retorna la cantidad de items eliminados.
        """
        wishlist = self.obtener_o_crear(cliente_id)
        deleted, _ = WishlistItem.objects.filter(wishlist=wishlist).delete()
        return deleted

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def contiene_producto(self, cliente_id, producto_id) -> bool:
        """Retorna True si el producto está en la wishlist del cliente."""
        try:
            wishlist = Wishlist.objects.get(cliente_id=cliente_id)
        except Wishlist.DoesNotExist:
            return False
        return WishlistItem.objects.filter(
            wishlist=wishlist,
            producto_id=producto_id,
        ).exists()
