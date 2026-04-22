# 📝 Roadmap Técnico: Implementación de Mixins (Cambios Exactos)

**Este archivo contiene todo el código listo para copiar/pegar.**

## 📋 Lista de Cambios Necesarios

### ✅ PASO 1: Crear Carpeta `core/`

```bash
backend/
├── config/
├── customers/
├── app_negocio/
└── core/                    ← CREAR
    ├── __init__.py          ← CREAR
    ├── mixins.py            ← CREAR
    ├── views.py             ← CREAR
```

---

### ✅ PASO 2: Crear `backend/core/__init__.py`

```python
from .mixins import (
    MultiTenantMixin,
    ValidacionesMixin,
    AuditoriaMixin,
    CRUDGenericoMixin,
)
from .views import BaseViewSet

__all__ = [
    'MultiTenantMixin',
    'ValidacionesMixin',
    'AuditoriaMixin',
    'CRUDGenericoMixin',
    'BaseViewSet',
]
```

---

### ✅ PASO 3: Crear `backend/core/mixins.py` (200 líneas)

```python
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import viewsets
from django.db import connection
from customers.services.bitacora_service import BitacoraService


# ═══════════════════════════════════════════════════════════
# 1️⃣ MIXIN: Multi-Tenant - Aislamiento por Schema
# ═══════════════════════════════════════════════════════════

class MultiTenantMixin:
    """
    Aislamiento automático por tenant (schema).
    ✅ Si schema='public' → sin datos
    ✅ Si schema='cliente1' → solo datos de cliente1
    """
    
    def get_queryset(self):
        """
        Filtra automáticamente por tenant actual.
        django-tenants aplica el filtro a nivel BD.
        """
        queryset = super().get_queryset()
        
        # Si estamos en schema 'public', retorna vacío
        if connection.schema_name == 'public':
            return queryset.none()
        
        # Si estamos en schema específico (cliente1, cliente2, etc.)
        # django-tenants automáticamente filtra por ese schema
        return queryset


# ═══════════════════════════════════════════════════════════
# 2️⃣ MIXIN: Validaciones - Reglas Globales
# ═══════════════════════════════════════════════════════════

class ValidacionesMixin:
    """
    Validaciones globales que aplican a TODOS los CRUDs.
    ✅ Usuario activo
    ✅ Permisos suficientes
    ✅ Datos válidos
    """
    
    def _validate_user_active(self):
        """Verificar que usuario está activo."""
        if not self.request.user.is_active:
            raise PermissionDenied(
                "Tu usuario está desactivado. Contacta al administrador."
            )
    
    def _validate_create_permission(self):
        """Verificar permisos para crear."""
        self._validate_user_active()
        # Aquí agregar validaciones específicas si es necesario
    
    def _validate_update_permission(self, instance):
        """Verificar permisos para editar."""
        self._validate_user_active()
        # Aquí agregar validaciones específicas si es necesario
    
    def _validate_destroy_permission(self, instance):
        """Verificar permisos para eliminar."""
        self._validate_user_active()
        # Por defecto, solo admin puede eliminar
        if not self.request.user.is_staff:
            raise PermissionDenied(
                "Solo administradores pueden eliminar registros."
            )
    
    def perform_create(self, serializer):
        """Ejecuta validaciones antes de crear."""
        self._validate_create_permission()
        super().perform_create(serializer)
    
    def perform_update(self, serializer):
        """Ejecuta validaciones antes de editar."""
        self._validate_update_permission(serializer.instance)
        super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        """Ejecuta validaciones antes de eliminar."""
        self._validate_destroy_permission(instance)
        super().perform_destroy(instance)


# ═══════════════════════════════════════════════════════════
# 3️⃣ MIXIN: Auditoría - Registra todas las acciones
# ═══════════════════════════════════════════════════════════

class AuditoriaMixin:
    """
    Auditoría automática: CREAR, EDITAR, ELIMINAR.
    ✅ Registra acción en Bitácora
    ✅ Incluye metadatos del objeto
    ✅ Funciona para todos los CRUDs
    """
    
    def get_audit_module_name(self):
        """
        Retorna el nombre del módulo para auditoría.
        Por defecto: nombre del modelo.
        
        Puede ser sobrescrito en ViewSet específico:
        def get_audit_module_name(self):
            return "Mi Módulo Personalizado"
        """
        model_name = self.queryset.model.__name__
        return model_name
    
    def get_audit_metadata_create(self, instance):
        """
        Retorna metadatos a registrar en auditoría.
        Puede ser sobrescrito en ViewSet específico.
        """
        return {
            'id': instance.id,
            'accion': 'CREAR'
        }
    
    def get_audit_metadata_update(self, instance):
        """Metadatos para actualización."""
        return {
            'id': instance.id,
            'accion': 'EDITAR'
        }
    
    def get_audit_metadata_destroy(self, instance):
        """Metadatos para eliminación."""
        return {
            'id': instance.id,
            'nombre_instancia': str(instance),
            'accion': 'ELIMINAR'
        }
    
    def perform_create(self, serializer):
        """Crea + Audita."""
        # 1. Crear registro
        instance = serializer.save()
        
        # 2. Registrar en auditoría
        BitacoraService.registrar_accion(
            usuario=self.request.user,
            modulo=self.get_audit_module_name(),
            accion='CREAR',
            metadatos=self.get_audit_metadata_create(instance)
        )
        
        # 3. Continuar con otros Mixins
        super().perform_create(serializer)
    
    def perform_update(self, serializer):
        """Edita + Audita."""
        # 1. Editar registro
        instance = serializer.save()
        
        # 2. Registrar en auditoría
        BitacoraService.registrar_accion(
            usuario=self.request.user,
            modulo=self.get_audit_module_name(),
            accion='EDITAR',
            metadatos=self.get_audit_metadata_update(instance)
        )
        
        # 3. Continuar con otros Mixins
        super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        """Elimina + Audita (en ese orden)."""
        # Guardar datos ANTES de eliminar (para auditoría)
        metadata = self.get_audit_metadata_destroy(instance)
        
        # Eliminar
        instance.delete()
        
        # Registrar en auditoría DESPUÉS de eliminar
        # (porque Bitácora está en schema 'public' y no se borra)
        BitacoraService.registrar_accion(
            usuario=self.request.user,
            modulo=self.get_audit_module_name(),
            accion='ELIMINAR',
            metadatos=metadata
        )
        
        # Continuar con otros Mixins
        super().perform_destroy(instance)


# ═══════════════════════════════════════════════════════════
# 4️⃣ MIXIN: CRUD Genérico - Combina los 3 anteriores
# ═══════════════════════════════════════════════════════════

class CRUDGenericoMixin(MultiTenantMixin, ValidacionesMixin, AuditoriaMixin):
    """
    Combina los 3 Mixins anteriores.
    
    Orden de ejecución en herencia múltiple (MRO):
    1. MultiTenantMixin (get_queryset)
    2. ValidacionesMixin (validaciones)
    3. AuditoriaMixin (auditoría)
    4. ModelViewSet (CRUD base)
    
    Resultado: Todo automático para cualquier ViewSet que herede.
    """
    pass
```

---

### ✅ PASO 4: Crear `backend/core/views.py`

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .mixins import CRUDGenericoMixin


class BaseViewSet(CRUDGenericoMixin, viewsets.ModelViewSet):
    """
    Base ViewSet que aplica a TODOS los CRUDs del proyecto.
    
    Características automáticas:
    ✅ Multi-tenant isolation (solo datos del schema actual)
    ✅ Validaciones globales (usuario activo, permisos)
    ✅ Auditoría automática (CREAR, EDITAR, ELIMINAR)
    ✅ Permisos de autenticación
    ✅ Paginación automática
    ✅ Filtros automáticos
    
    Uso:
    
    class MiViewSet(BaseViewSet):
        queryset = MiModelo.objects.all()
        serializer_class = MiSerializer
    
    ¡Listo! 12 líneas de código, todo el resto automático.
    """
    
    permission_classes = [IsAuthenticated]
    
    # Paginación por defecto (personalizable)
    # pagination_class = CustomPagination
    
    # Filtros por defecto (personalizable)
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    # search_fields = ['nombre', 'descripcion']
    # filterset_fields = ['activo', 'categoria']
```

---

### ✅ PASO 5: Refactorizar ProductoViewSet

**Ruta:** `backend/app_negocio/views/producto_views.py`

**NUEVO CONTENIDO (Reemplazar todo):**

```python
from core.views import BaseViewSet
from app_negocio.models.producto import Producto
from app_negocio.serializers.producto_serializer import ProductoSerializer


class ProductoViewSet(BaseViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
```

---

### ✅ PASO 6: Ejecutar Migraciones

```bash
cd backend

# Compilar syntax
python -m py_compile core/mixins.py
python -m py_compile core/views.py

# Migraciones (sin cambios en BD)
python manage.py migrate_schemas

# Verificar
python manage.py runserver
# GET /api/productos/ debe funcionar ✅
```

---

## ✅ Verificación Final

```python
# Terminal
python manage.py shell

# Importar y verificar
from core import BaseViewSet, CRUDGenericoMixin
from app_negocio.views.producto_views import ProductoViewSet

# Debe mostrar que ProductoViewSet hereda de BaseViewSet
print(ProductoViewSet.__bases__)
# Output: (<class 'core.views.BaseViewSet'>,)

# Verificar MRO (Method Resolution Order)
print(ProductoViewSet.__mro__)
# Debe mostrar: ProductoViewSet → BaseViewSet → CRUDGenericoMixin → ... → object
```

---

**¡Completado!** Ahora puedes crear nuevos CRUDs con 12 líneas. Ver `05_FASES_EJECUCION.md` para la guía paso a paso.
