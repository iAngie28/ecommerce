from django.http import JsonResponse
from django.db import connection
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from app_negocio.views.producto_views import ProductoViewSet
from customers.views.usuario_views import MyTokenObtainPairView, LogoutView

# Debug temporal
def debug_schema(request):
    return JsonResponse({'urlconf': 'config.tenant_urls', 'schema': connection.schema_name})

# URLs explícitas SIN usar DefaultRouter para evitar conflictos de nombre con config.urls
urlpatterns = [
    path('api/debug/', debug_schema),

    # Auth
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    # Productos - paths explícitos, sin DefaultRouter
    path('api/productos/', ProductoViewSet.as_view({'get': 'list', 'post': 'create'}), name='producto-list'),
    path('api/productos/<int:pk>/', ProductoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='producto-detail'),
]
