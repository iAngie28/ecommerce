from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app_negocio.views.producto_views import ProductoViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from customers.views.usuario_views import (
    MyTokenObtainPairView, LogoutView, UsuarioCrudViewSet,
    PasswordResetRequestView, PasswordResetConfirmView,
    TenantListView, TenantCreateView
)

# 1. Configuramos el enrutador de la API
router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='productos')
router.register(r'usuarios', UsuarioCrudViewSet, basename='usuarios')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. Rutas para autenticación JWT
    # CAMBIO: Usamos MyTokenObtainPairView en lugar de la vista por defecto
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # 3. Incluimos las rutas de nuestra API de negocio (Productos)
    path('api/', include(router.urls)),


    path('api/tiendas/', TenantListView.as_view()),
    path('api/tiendas/crear/', TenantCreateView.as_view()),
]