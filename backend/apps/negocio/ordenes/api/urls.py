# apps/negocio/ordenes/api/urls.py
from django.urls import path
from app_negocio.views.carrito_views import CarritoViewSet
from app_negocio.views.pedido_views import PedidoViewSet

urlpatterns = [
    # Carritos
    path('carritos/', CarritoViewSet.as_view({'get': 'list', 'post': 'create'}), name='carrito-list'),
    path('carritos/<int:pk>/', CarritoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='carrito-detail'),
    path('carritos/<int:pk>/agregar-item/', CarritoViewSet.as_view({'post': 'agregar_item'}), name='carrito-agregar-item'),
    path('carritos/<int:pk>/eliminar-item/', CarritoViewSet.as_view({'post': 'eliminar_item'}), name='carrito-eliminar-item'),
    path('carritos/<int:pk>/vaciar/', CarritoViewSet.as_view({'post': 'vaciar'}), name='carrito-vaciar'),
    path('carritos/<int:pk>/cerrar/', CarritoViewSet.as_view({'post': 'cerrar'}), name='carrito-cerrar'),
    # Pedidos
    path('pedidos/', PedidoViewSet.as_view({'get': 'list', 'post': 'create'}), name='pedido-list'),
    path('pedidos/<int:pk>/', PedidoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='pedido-detail'),
    path('pedidos/crear-desde-carrito/', PedidoViewSet.as_view({'post': 'crear_desde_carrito'}), name='pedido-desde-carrito'),
    path('pedidos/<int:pk>/cambiar-estado/', PedidoViewSet.as_view({'post': 'cambiar_estado'}), name='pedido-cambiar-estado'),
]
