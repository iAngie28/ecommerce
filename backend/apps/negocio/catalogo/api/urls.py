# apps/negocio/catalogo/api/urls.py
from django.urls import path
from app_negocio.views.producto_views import ProductoViewSet
from app_negocio.views.categoria_views import CategoriaViewSet

urlpatterns = [
    path('productos/', ProductoViewSet.as_view({'get': 'list', 'post': 'create'}), name='producto-list'),
    path('productos/<int:pk>/', ProductoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='producto-detail'),
    path('categorias/', CategoriaViewSet.as_view({'get': 'list', 'post': 'create'}), name='categoria-list'),
    path('categorias/<int:pk>/', CategoriaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='categoria-detail'),
]
