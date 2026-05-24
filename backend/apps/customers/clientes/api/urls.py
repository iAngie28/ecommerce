# apps/customers/clientes/api/urls.py
from django.urls import path
from apps.customers.views.cliente_views import ClienteViewSet, ClienteLoginView
from apps.customers.views.device_token_views import DeviceTokenRegisterView

urlpatterns = [
    path('clientes/login/', ClienteLoginView.as_view(), name='cliente_login'),
    path('clientes/', ClienteViewSet.as_view({'get': 'list', 'post': 'create'}), name='clientes-list'),
    path('clientes/<int:pk>/', ClienteViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('clientes/perfil/', ClienteViewSet.as_view({'get': 'perfil', 'patch': 'perfil'}), name='cliente-perfil'),
]
