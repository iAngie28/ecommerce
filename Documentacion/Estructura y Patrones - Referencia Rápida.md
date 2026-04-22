
# Estructura y Patrones - Referencia Rápida para Desarrolladores
<img width="2752" height="1536" alt="unnamed (1)" src="https://github.com/user-attachments/assets/e1367603-f583-4ab9-8745-280065eb6dd4" />
**Objetivo:** Guía rápida para entender dónde va cada cosa y cómo implementar nuevas funcionalidades.

---

## 1. ¿QUÉ ES UN MIXIN?
<img width="2752" height="1536" alt="mixin" src="https://github.com/user-attachments/assets/783a681b-68f6-4753-adbb-bb488d3f0d2c" />

Un **Mixin** es una clase pequeña que "inyecta" funcionalidad reutilizable en otras clases sin necesidad de repetir código.

### Analogía

```python
# ❌ SIN MIXIN (Repetición)
class ProductoViewSet(ModelViewSet):
    def perform_create(self, serializer):
        instancia = serializer.save()
        # Auditoría manual aquí
        BitacoraService.registrar_accion(...)
    
    def perform_update(self, serializer):
        instancia = serializer.save()
        # Auditoría manual aquí (REPETIDA)
        BitacoraService.registrar_accion(...)

class UsuarioCrudViewSet(ModelViewSet):
    def perform_create(self, serializer):
        instancia = serializer.save()
        # Auditoría manual aquí (REPETIDA)
        BitacoraService.registrar_accion(...)

# ✅ CON MIXIN (DRY - Don't Repeat Yourself)
class AuditoriaMixin:
    def perform_create(self, serializer):
        instancia = serializer.save()
        BitacoraService.registrar_accion(...)
    def perform_update(self, serializer):
        instancia = serializer.save()
        BitacoraService.registrar_accion(...)

class ProductoViewSet(AuditoriaMixin, ModelViewSet):
    pass  # ✅ Auditoría automática

class UsuarioCrudViewSet(AuditoriaMixin, ModelViewSet):
    pass  # ✅ Auditoría automática
```

**Regla de Oro:** Si una responsabilidad se repite en +2 ViewSets, va en un Mixin.

---

## 2. MIXINS EN ESTE PROYECTO

### Mixin: AuditoriaMixin

**¿Qué hace?** Registra automáticamente todas las acciones (CREAR, EDITAR, ELIMINAR) en la Bitácora.

```python
class AuditoriaMixin:
    modulo_auditoria = None  # La ViewSet hija debe definir esto
    
    def perform_create(self, serializer):
        instancia = serializer.save()
        if self.modulo_auditoria:
            BitacoraService.registrar_accion(
                self.request.user, self.modulo_auditoria, "CREAR",
                request=self.request,
                metadatos={'id': instancia.id}
            )
    
    def perform_update(self, serializer):
        instancia = serializer.save()
        if self.modulo_auditoria:
            BitacoraService.registrar_accion(
                self.request.user, self.modulo_auditoria, "EDITAR",
                request=self.request,
                metadatos={'id': instancia.id}
            )
    
    def perform_destroy(self, instance):
        id_instancia = instance.id
        instance.delete()
        if self.modulo_auditoria:
            BitacoraService.registrar_accion(
                self.request.user, self.modulo_auditoria, "ELIMINAR",
                request=self.request,
                metadatos={'id': id_instancia}
            )
```

**¿Quién lo usa?** Todas las ViewSets que necesiten auditoría automática.

**¿Beneficio?** NO necesitas escribir `BitacoraService.registrar_accion()` en cada método. El Mixin lo hace automáticamente.

**¿Y la Multi-tenancia?** `django-tenants` ya lo maneja automáticamente a través del middleware. No requiere mixin adicional.

## 3. ESTRUCTURA DE CARPETAS: ¿POR QUÉ ASÍ?

```
backend/
├── core/                     ← INFRAESTRUCTURA (COMPARTIDA)
│   ├── mixins.py             [AuditoriaMixin]
│   ├── views.py              [BaseViewSet que hereda de AuditoriaMixin]
│   ├── services.py           [BaseService con CRUD genérico]
│   ├── validators.py         [Validadores centralizados]
│   └── exceptions.py         [Excepciones de negocio]
│
├── customers/                ← APP COMPARTIDA (Usuarios, Tenants)
│   ├── models/
│   │   ├── usuario.py        [Modelo Usuario]
│   │   ├── tenant.py         [Modelo Client/Tenant]
│   │   └── bitacora.py       [Auditoría central]
│   ├── services/
│   │   ├── usuario_service.py [Lógica de usuarios]
│   │   ├── auth_service.py    [Lógica de autenticación]
│   │   └── bitacora_service.py [Lógica de auditoría]
│   ├── serializers/
│   │   └── usuario_serializers.py [Conversión a JSON]
│   ├── views/
│   │   └── usuario_views.py  [UsuarioCrudViewSet - hereda BaseViewSet]
│   └── admin/
│       └── base.py           [TenantSafeAdmin - seguridad multi-tenant]
│
└── app_negocio/              ← APP DE NEGOCIO (Productos, Ventas)
    ├── models/
    │   └── producto.py       [Modelo Producto]
    ├── services/
    │   └── producto_service.py [Lógica de productos]
    ├── serializers/
    │   └── producto_serializer.py [Conversión a JSON]
    ├── views/
    │   └── producto_views.py [ProductoViewSet - hereda BaseViewSet]
    └── admin/
        └── producto_admin.py [ProductoAdmin - hereda TenantSafeAdmin]
```

### ¿Por qué esta estructura?

| Carpeta | ¿Por qué? | Regla |
|---------|----------|-------|
| **core/** | Una sola vez (DRY) | Todo que sea reutilizable aquí |
| **models/** | Separación de responsabilidades | Cada entidad en su archivo |
| **services/** | Lógica de negocio centralizada | NO duplicar lógica |
| **serializers/** | Conversión a JSON + validaciones básicas | NO decisiones de negocio |
| **views/** | Orquestadores HTTP | Heredan de `BaseViewSet` |
| **admin/** | Interfaz administrativa | Heredan de `TenantSafeAdmin` |

---

## 4. FLUJO DE INFORMACIÓN

### Caso: POST /api/productos/ (Crear Producto)

```
1. REQUEST HTTP
   └─ Llega: POST /api/productos/
              JSON: {"nombre": "Laptop", "precio": 1200, "stock": 5}

2. MULTITENANT MIDDLEWARE
   └─ django-tenants intercepta
   └─ Lee Host: cliente1.localhost
   └─ Conecta a schema: cliente1
   └─ Ahora todas las queries filtran por ese schema

3. ROUTEADOR (urls.py)
   └─ Dirige a: ProductoViewSet

4. VISTA (ProductoViewSet)
   └─ Hereda de BaseViewSet
      └─ AuditoriaMixin ✅ (auditoría automática)
      └─ (Multi-tenancia: manejada automáticamente por django-tenants)
   
   └─ Llama: perform_create(serializer)
      ├─ Serializer valida JSON
      ├─ Luego Service ejecuta lógica
      └─ AuditoriaMixin registra acción automáticamente

5. SERIALIZER (ProductoSerializer)
   └─ Valida que el JSON sea correcto
   └─ Convierte a objetos Python
   └─ Si hay error, devuelve 400 Bad Request

6. SERVICE (ProductoService)
   └─ Hereda de BaseService
   └─ Ejecuta: crear(datos_validados)
   └─ Lógica de negocio aquí
   └─ Guarda en BD (con transacción automática)

7. AUDITORÍA (AuditoriaMixin)
   └─ Registra: 
      - Usuario: request.user
      - Módulo: "Producto"
      - Acción: "CREAR"
      - Metadatos: {'id': 1}
   └─ Guarda en Bitacora

8. RESPONSE HTTP
   └─ JSON con producto creado + status 201
   └─ Frontend recibe y actualiza UI
```

### Comparativa: ¿Qué cambió?

**ANTES (Manual):**
- 50 líneas en ProductoViewSet
- Auditoría manual en cada método (repetida)
- Filtro manual por schema

**AHORA (Con Mixins):**
- 8 líneas en ProductoViewSet
- Auditoría automática (cero líneas)
- Filtro automático (Mixin)

---

## 5. CÓMO IMPLEMENTAR ALGO NUEVO

### Escenario: Quieres crear un nuevo CRUD (Ej: Categorías)

**Paso 1: Crear Modelo**
```python
# app_negocio/models/categoria.py
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
```

**Paso 2: Crear Serializer**
```python
# app_negocio/serializers/categoria_serializer.py
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']  # ✅ Lista explícita
```

**Paso 3: Crear Service**
```python
# app_negocio/services/categoria_service.py
from core.services import BaseService

class CategoriaService(BaseService):
    def __init__(self):
        super().__init__(Categoria)
    
    # Si necesitas lógica especial, agrégala aquí
    def crear_con_validacion(self, datos):
        # Tu lógica de negocio
        return self.crear(datos)
```

**Paso 4: Crear View**
```python
# app_negocio/views/categoria_views.py
from core.views import BaseViewSet

class CategoriaViewSet(BaseViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    modulo_auditoria = "Categoria"  # ✅ Para AuditoriaMixin
    
    # ✅ AuditoriaMixin automático + Multi-tenancia via django-tenants
    # ✅ CRUD completo heredado de BaseViewSet
```

**Paso 5: Registrar en URLs**
```python
# config/urls.py
from rest_framework.routers import DefaultRouter
from app_negocio.views.categoria_views import CategoriaViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**¡LISTO!** Ya tienes:
- ✅ CRUD completo (GET, POST, PUT, DELETE)
- ✅ Multi-tenant automático
- ✅ Auditoría automática
- ✅ Validaciones
- ✅ Transacciones automáticas

**Total: ~30 líneas de código para un CRUD completo.**

---

## 6. REGLAS DE ORO

| Regla | Razón |
|-------|-------|
| **Modelos:** Sin lógica de negocio | Solo estructura de datos |
| **Serializers:** Solo validaciones básicas | No decisiones de negocio |
| **Services:** Toda la lógica aquí | Un solo lugar para cambiar |
| **Views:** Heredan de BaseViewSet | Auditoría + Multi-tenant automáticos |
| **Core/:** Una sola vez | Reutilizable en todos los CRUDs |
| **Mixins:** No repitas +2 veces | Si repites, crea un Mixin |

---

## 7. RESUMEN FINAL

```
┌─────────────────────────────────────────────────────────┐
│ REQUEST HTTP (ej: POST /api/productos/)                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ MultiTenant Filter │ ← Mixin
        │ (por schema)       │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │ ProductoViewSet        │ ← Hereda BaseViewSet
        │ (orquestador)          │
        └────┬───────────────────┘
             │
             ├─→ Serializer       ← Valida JSON
             │
             ├─→ ProductoService  ← Lógica de negocio
             │                      (hereda BaseService)
             │
             └─→ AuditoriaMixin   ← Registra acción automáticamente
                 (CREAR/EDITAR/ELIMINAR)

BENEFICIO: Cero duplication, máxima reutilización.
TIEMPO: Un CRUD = 15 minutos.
```

---

## 📌 REFERENCIAS RÁPIDAS

**¿Dónde agrego un endpoint especial?** 
→ En la View, crea un `@action`

**¿Dónde agrego validación personalizada?**
→ En el Service o en el Validator

**¿Dónde agrego lógica de auditoría especial?**
→ Override `perform_*` en la View

**¿Dónde agrego un filtro especial?**
→ Override `get_queryset()` en la View

**¿Cómo cambio la auditoría globalmente?**
→ Edita `core/mixins.py` (un solo lugar)

---

**Última actualización:** 21 de Abril, 2026  
**Estado:** Arquitectura basada en Mixins y Clean Architecture ✅
