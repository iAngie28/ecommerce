from django.contrib import admin
from django.urls import path, include # Agregamos include
from rest_framework.routers import DefaultRouter # Importamos el router de DRF
from app_negocio.views import ProductoViewSet # Importamos tu vista de la API

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 

# 1. Configuramos el enrutador de la API
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. Rutas para autenticación JWT (lo que React usará para el Login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

    # 3. Incluimos las rutas de nuestra API de negocio
    path('api/', include(router.urls)), # [cite: 219]
]