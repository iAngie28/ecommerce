from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.gestionDeUsuarioySeguridad.cu1_iniciar_sesion.authentication import (
    ClienteJWTAuthentication,
    UsuarioJWTAuthentication,
)
from apps.customers.models import Cliente
from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.api.serializers import WishlistSerializer
from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.services.wishlist_service import WishlistService


class WishlistViewSet(ViewSet):
    """
    API de Lista de Deseos (Wishlist) — CU25.

    Todos los endpoints operan sobre la wishlist del cliente autenticado.
    Un usuario administrador/vendedor también puede consultar (solo lectura).

    Endpoints:
        GET  /api/wishlist/                      → Ver mi wishlist completa
        POST /api/wishlist/agregar/              → Agregar producto { "producto_id": X }
        DELETE /api/wishlist/eliminar/<id>/      → Eliminar producto de la wishlist
        POST /api/wishlist/toggle/<id>/          → Agregar si no existe, eliminar si existe
        POST /api/wishlist/mover-al-carrito/<id>/→ Mover producto al carrito activo
        GET  /api/wishlist/contiene/<id>/        → ¿Está este producto en mi wishlist?
        DELETE /api/wishlist/vaciar/             → Vaciar toda la wishlist
    """

    authentication_classes = [ClienteJWTAuthentication, UsuarioJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_service(self):
        return WishlistService()

    def _get_cliente(self):
        """Retorna el Cliente del schema actual usando correo como llave estable."""
        auth = getattr(self.request, 'auth', None)
        if hasattr(auth, 'get') and auth.get('role') == 'CLIENTE':
            correo = auth.get('correo') or getattr(self.request.user, 'correo', None)
            if correo:
                cliente = Cliente.objects.filter(correo=correo).first()
                if cliente:
                    return cliente

            cliente_id = auth.get('cliente_id') or auth.get('user_id')
            if cliente_id:
                return Cliente.objects.filter(id=cliente_id).first()
        return None

    def _get_cliente_id(self):
        cliente = self._get_cliente()
        return cliente.id if cliente else None

    def _get_cliente_en_schema_actual(self, cliente):
        if not cliente:
            return None

        correo = getattr(cliente, 'correo', None)
        if correo:
            cliente_schema = Cliente.objects.filter(correo=correo).first()
            if cliente_schema:
                return cliente_schema

        return Cliente.objects.filter(id=cliente.id).first()

    def _get_tenant_host(self, tenant):
        domain = tenant.domains.first()
        return getattr(domain, 'domain', None) or tenant.schema_name

    # ------------------------------------------------------------------
    # GET /api/wishlist/
    # ------------------------------------------------------------------

    def list(self, request):
        """Retorna la wishlist completa del cliente autenticado (agrupada si es público)."""
        from django.db import connection
        
        cliente = self._get_cliente()
        if not cliente:
            return Response(
                {'error': 'Solo los clientes pueden acceder a su lista de deseos.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Si es el esquema público, buscamos en todos los tenants
        if connection.schema_name == 'public':
            from apps.customers.models import Client
            from django_tenants.utils import tenant_context
            from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist import Wishlist
            
            todos_items = []
            for tenant in Client.objects.exclude(schema_name='public'):
                tenant_host = self._get_tenant_host(tenant)
                with tenant_context(tenant):
                    try:
                        cliente_tenant = self._get_cliente_en_schema_actual(cliente)
                        if not cliente_tenant:
                            continue

                        wishlist = Wishlist.objects.get(cliente_id=cliente_tenant.id)
                        if wishlist.items.exists():
                            serializer = WishlistSerializer(wishlist, context={'request': request})
                            items_data = serializer.data.get('items', [])
                            for item in items_data:
                                item['tienda_nombre'] = (
                                    getattr(tenant, 'nombre_comercial', None)
                                    or getattr(tenant, 'name', None)
                                    or tenant.schema_name
                                )
                                item['tienda_schema'] = tenant.schema_name
                                item['tienda_host'] = tenant_host
                                todos_items.append(item)
                    except Wishlist.DoesNotExist:
                        pass
            
            return Response({'items': todos_items, 'total_items': len(todos_items)}, status=status.HTTP_200_OK)
            
        cliente_id = self._get_cliente_id()
        try:
            wishlist = self.get_service().obtener_o_crear(cliente_id)
            serializer = WishlistSerializer(wishlist, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # POST /api/wishlist/agregar/
    # ------------------------------------------------------------------

    @action(detail=False, methods=['post'], url_path='agregar')
    def agregar(self, request):
        """Agrega un producto a la wishlist. Body: { "producto_id": <int> }"""
        cliente_id = self._get_cliente_id()
        if not cliente_id:
            return Response(
                {'error': 'Solo los clientes pueden modificar su lista de deseos.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        producto_id = request.data.get('producto_id')
        if not producto_id:
            return Response(
                {'error': 'El campo producto_id es requerido.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            self.get_service().agregar_producto(cliente_id, producto_id)
            wishlist = self.get_service().obtener_o_crear(cliente_id)
            serializer = WishlistSerializer(wishlist, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # DELETE /api/wishlist/eliminar/<producto_id>/
    # ------------------------------------------------------------------

    @action(detail=False, methods=['delete'], url_path=r'eliminar/(?P<producto_id>\d+)')
    def eliminar(self, request, producto_id=None):
        """Elimina un producto de la wishlist del cliente."""
        cliente_id = self._get_cliente_id()
        if not cliente_id:
            return Response(
                {'error': 'Solo los clientes pueden modificar su lista de deseos.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            self.get_service().eliminar_producto(cliente_id, producto_id)
            wishlist = self.get_service().obtener_o_crear(cliente_id)
            serializer = WishlistSerializer(wishlist, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # POST /api/wishlist/toggle/<producto_id>/
    # ------------------------------------------------------------------

    @action(detail=False, methods=['post'], url_path=r'toggle/(?P<producto_id>\d+)')
    def toggle(self, request, producto_id=None):
        """
        Toggle: agrega el producto si no está en la wishlist,
        lo elimina si ya existe.
        Responde: { "accion": "agregado"|"eliminado", "wishlist": {...} }
        """
        cliente_id = self._get_cliente_id()
        if not cliente_id:
            return Response(
                {'error': 'Solo los clientes pueden modificar su lista de deseos.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            resultado = self.get_service().toggle_producto(cliente_id, producto_id)
            wishlist = self.get_service().obtener_o_crear(cliente_id)
            serializer = WishlistSerializer(wishlist, context={'request': request})
            return Response(
                {**resultado, 'wishlist': serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # POST /api/wishlist/mover-al-carrito/<producto_id>/
    # ------------------------------------------------------------------

    @action(detail=False, methods=['post'], url_path=r'mover-al-carrito/(?P<producto_id>\d+)')
    def mover_al_carrito(self, request, producto_id=None):
        """
        Mueve el producto del wishlist al carrito activo del cliente
        y lo elimina de la lista de deseos.
        """
        cliente_id = self._get_cliente_id()
        if not cliente_id:
            return Response(
                {'error': 'Solo los clientes pueden realizar esta acción.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            self.get_service().mover_al_carrito(cliente_id, producto_id)
            wishlist = self.get_service().obtener_o_crear(cliente_id)
            serializer = WishlistSerializer(wishlist, context={'request': request})
            return Response(
                {'mensaje': 'Producto movido al carrito correctamente.', 'wishlist': serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # GET /api/wishlist/contiene/<producto_id>/
    # ------------------------------------------------------------------

    @action(detail=False, methods=['get'], url_path=r'contiene/(?P<producto_id>\d+)')
    def contiene(self, request, producto_id=None):
        """
        Consulta rápida para el botón de corazón en las tarjetas de producto.
        Responde: { "en_wishlist": true|false }
        """
        cliente_id = self._get_cliente_id()
        if not cliente_id:
            return Response({'en_wishlist': False}, status=status.HTTP_200_OK)
        en_wishlist = self.get_service().contiene_producto(cliente_id, producto_id)
        return Response({'en_wishlist': en_wishlist}, status=status.HTTP_200_OK)

    # ------------------------------------------------------------------
    # DELETE /api/wishlist/vaciar/
    # ------------------------------------------------------------------

    @action(detail=False, methods=['delete'], url_path='vaciar')
    def vaciar(self, request):
        """Vacía toda la lista de deseos del cliente."""
        from django.db import connection

        cliente = self._get_cliente()
        if not cliente:
            return Response(
                {'error': 'Solo los clientes pueden vaciar su lista de deseos.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if connection.schema_name == 'public':
            from apps.customers.models import Client
            from django_tenants.utils import tenant_context
            from apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.models.wishlist_item import WishlistItem

            eliminados = 0
            for tenant in Client.objects.exclude(schema_name='public'):
                with tenant_context(tenant):
                    cliente_tenant = self._get_cliente_en_schema_actual(cliente)
                    if not cliente_tenant:
                        continue
                    deleted, _ = WishlistItem.objects.filter(
                        wishlist__cliente_id=cliente_tenant.id,
                    ).delete()
                    eliminados += deleted

            return Response(
                {'mensaje': f'Lista de deseos vaciada. {eliminados} producto(s) eliminado(s).'},
                status=status.HTTP_200_OK,
            )

        cliente_id = cliente.id
        try:
            eliminados = self.get_service().vaciar(cliente_id)
            return Response(
                {'mensaje': f'Lista de deseos vaciada. {eliminados} producto(s) eliminado(s).'},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
