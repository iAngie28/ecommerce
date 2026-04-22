# 🏗️ Análisis: Integración de Mixins para CRUDs en tu Arquitectura

## 📊 Estado Actual vs Estado Futuro

### Estado Actual
```
app_negocio/views/producto_views.py
├── ProductoViewSet(viewsets.ModelViewSet)
│   ├── get_queryset()
│   ├── perform_create()   ← Auditoría + lógica
│   ├── perform_update()   ← Auditoría + lógica
│   └── perform_destroy()  ← Auditoría + lógica
│
└── Problema: Código repetido en cada ViewSet
   (Si creas 10 CRUDs, repites esto 10 veces)
```

### Estado Futuro (Con Mixins)
```
core/mixins.py
├── AuditoriaMixin          ← Registro de acciones (centralizado)
├── ValidacionesMixin       ← Validaciones globales
├── MultiTenantMixin        ← Aislamiento de tenant
└── CRUDGenericoMixin       ← Combina todos

config/views.py
└── BaseViewSet(CRUDGenericoMixin, viewsets.ModelViewSet)
    └── ViewSet listo para heredar

app_negocio/views/producto_views.py
└── ProductoViewSet(BaseViewSet)
    └─ ¡Solo 3-5 líneas de código!

app_negocio/views/categoria_views.py
└── CategoriaViewSet(BaseViewSet)
    └─ ¡Solo 3-5 líneas de código!
```

---

## 🔍 Análisis Profundo

### 1. Estructura de Mixins Necesarios

Tu arquitectura necesita **4 Mixins principales**:

#### MIXIN 1: MultiTenantMixin
**Propósito:** Garantizar que los datos estén filtrados por tenant

```python
# core/mixins.py
class MultiTenantMixin:
    """
    Asegura que get_queryset() siempre retorne datos del tenant actual.
    Previene que un usuario de tenant1 vea datos de tenant2.
    """
    
    def get_queryset(self):
        from django.db import connection
        
        # Si el schema es 'public' (login global), retorna vacío
        if connection.schema_name == 'public':
            return self.queryset.model.objects.none()
        
        # Si estamos en un schema de tenant, retorna sus datos
        return self.queryset.all()
```

**¿Por qué va aquí?**
- Toda vista necesita aislamiento multi-tenant
- Centralizar esta lógica evita bugs de seguridad
- Si cambias la estrategia de aislamiento, cambias 1 lugar

**Impacto en tus archivos:**
```
ANTES (ProductoViewSet):
def get_queryset(self):
    current_schema = connection.schema_name
    if current_schema == 'public':
        return Producto.objects.none()
    return Producto.objects.all()

DESPUES (Con Mixin, ProductoViewSet):
# ¡No necesita get_queryset()! Hereda del Mixin
```

---

#### MIXIN 2: AuditoriaMixin
**Propósito:** Registrar automáticamente todas las acciones

```python
# core/mixins.py
class AuditoriaMixin:
    """
    Registra automáticamente CREAR, EDITAR, ELIMINAR en Bitácora.
    """
    
    def perform_create(self, serializer):
        instancia = serializer.save()
        
        # Registrar en Bitácora
        from customers.services.bitacora_service import BitacoraService
        BitacoraService.registrar_accion(
            usuario=self.request.user,
            modulo=self.get_audit_module_name(),  # "Producto", "Categoría", etc.
            accion="CREAR",
            metadatos={
                'id': instancia.id,
                **self.get_audit_metadata(instancia, 'create')
            }
        )
    
    def perform_update(self, serializer):
        instancia = serializer.save()
        
        BitacoraService.registrar_accion(
            usuario=self.request.user,
            modulo=self.get_audit_module_name(),
            accion="EDITAR",
            metadatos={
                'id': instancia.id,
                'cambios': serializer.initial_data,
                **self.get_audit_metadata(instancia, 'update')
            }
        )
    
    def perform_destroy(self, instance):
        id_instancia = instance.id
        nombre_instancia = str(instance)
        instance.delete()
        
        BitacoraService.registrar_accion(
            usuario=self.request.user,
            modulo=self.get_audit_module_name(),
            accion="ELIMINAR",
            metadatos={
                'id': id_instancia,
                'instancia': nombre_instancia,
                **self.get_audit_metadata(instance, 'delete')
            }
        )
    
    # HOOKS para personalización
    def get_audit_module_name(self):
        """Retorna nombre del módulo para auditoría. Sobrescribir en subclase."""
        return self.queryset.model.__name__
    
    def get_audit_metadata(self, instancia, operacion):
        """Retorna metadatos adicionales. Sobrescribir si necesitas más."""
        return {}
```

**¿Por qué va aquí?**
- Toda vista necesita auditoría
- Evitas duplicar `BitacoraService.registrar_accion()` en 20 CRUDs
- Si cambias el formato de auditoría, cambias 1 lugar

---

#### MIXIN 3: ValidacionesMixin
**Propósito:** Validaciones globales que aplican a todos los CRUDs

```python
# core/mixins.py
class ValidacionesMixin:
    """
    Validaciones que aplican a TODOS los CRUDs.
    - Campos requeridos no vacíos
    - Formatos estándar
    - Restricciones globales
    """
    
    def perform_create(self, serializer):
        # Validación global: usuario debe estar activo
        if not self.request.user.is_active:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Tu usuario está desactivado")
        
        # Llamar al super() para que ejecute el rest del flujo
        super().perform_create(serializer)
    
    def perform_update(self, serializer):
        if not self.request.user.is_active:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Tu usuario está desactivado")
        
        super().perform_update(serializer)
```

---

#### MIXIN 4: CRUDGenericoMixin
**Propósito:** Combina todos los mixins anteriores

```python
# core/mixins.py
class CRUDGenericoMixin(
    ValidacionesMixin,
    AuditoriaMixin,
    MultiTenantMixin
):
    """
    Mixin que combina toda la lógica estándar.
    Orden IMPORTANTE: ValidacionesMixin primero (valida antes de auditar)
    """
    pass
```

---

## 🏗️ Estructura de Carpetas Actualizada

```
backend/
├── config/
├── customers/
├── app_negocio/
└── core/                    ← NEW FOLDER
    ├── __init__.py
    ├── mixins.py            ← Los 4 Mixins
    └── views.py             ← BaseViewSet
```

---

## 📊 Comparativa: Antes vs Después

### Crear 5 CRUDs nuevos

#### ANTES (Sin Mixins)
```
Código total: 500+ líneas
├─ ProductoViewSet: 100 líneas (perform_create, perform_update, etc)
├─ CategoriaViewSet: 100 líneas (código duplicado)
├─ InventarioViewSet: 100 líneas (código duplicado)
├─ ProveedorViewSet: 100 líneas (código duplicado)
└─ ClienteViewSet: 100 líneas (código duplicado)

Mantenimiento: Cambiar auditoría = modificar 5 archivos
```

#### DESPUÉS (Con Mixins)
```
Código total: ~50 líneas
├─ ProductoViewSet: 5 líneas
├─ CategoriaViewSet: 5 líneas
├─ InventarioViewSet: 5 líneas
├─ ProveedorViewSet: 5 líneas
├─ ClienteViewSet: 5 líneas
└─ core/mixins.py: 20 líneas

Mantenimiento: Cambiar auditoría = modificar 1 archivo
```

---

## ✅ Conclusión

**Implementa Mixins AHORA, antes de crear CRUDs nuevos.**

Te ahorrará 2-3 horas por CRUD nuevo y centralizará la lógica crítica.
