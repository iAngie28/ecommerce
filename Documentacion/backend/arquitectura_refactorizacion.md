# Arquitectura y Refactorización del Backend (2026)

## 1. Visión General

El backend ha sido refactorizado desde una estructura monolítica a una arquitectura modular orientada al dominio. Esto nos permite mantener el código más limpio, facilitar pruebas y evitar colisiones cuando varios desarrolladores trabajan al mismo tiempo. Además, utilizamos `django-tenants` para soportar escenarios SaaS (cada tienda tiene su propio esquema de base de datos) y un esquema `public` para configuraciones globales.

## 2. Estructura de Directorios

La carpeta principal es `apps/`, que contiene tres módulos principales (Dominios):

```text
backend/
├── apps/
│   ├── core/                  # Utilidades compartidas, clases base, mixins (Auditoria, BaseViewSet)
│   ├── customers/             # Módulo de "SaaS y Clientes" (Usuarios, Tenants, Auditoría, Clientes)
│   │   ├── audit/             # Bitácora, Backups, Restauración
│   │   ├── clientes/          # Modelo de Clientes (compradores)
│   │   ├── tenants/           # Modelos de Tenant (Tiendas) y Planes
│   │   └── users/             # Autenticación, Roles, Permisos, Usuario Vendedor/Admin
│   ├── negocio/               # Módulo "Core de Tienda" (Catálogo, Órdenes, Facturación)
│   │   ├── billing/           # Pagos, Facturas, Stripe
│   │   ├── catalogo/          # Productos, Categorías
│   │   ├── notificaciones/    # Notificaciones push (FCM) y en tiempo real
│   │   └── ordenes/           # Carritos, Pedidos, Items
│   └── voice/                 # Funcionalidades de IA (Antigravity SDK, Voz)
├── config/                    # Configuración global de Django (settings, urls principales, api_router)
└── requirements.txt
```

## 3. Patrones de Diseño

Hemos implementado el patrón **Service Layer** (Capa de Servicios) para extraer la lógica de negocio de los Controladores (ViewSets).

### 3.1. Modelos (Models)
Los modelos solo deben contener la definición de la base de datos y métodos muy simples (ej. `@property` para calcular un subtotal). No deben realizar consultas complejas o llamadas a APIs externas.

### 3.2. Capa de Servicios (Services)
Toda regla de negocio (ej. "descontar inventario", "marcar pedido como pagado", "validar stock") va en un archivo `_service.py`.
- **Ejemplo**: `apps.negocio.ordenes.services.pedido_service.PedidoService`
Los servicios heredan de `BaseService` de `apps.core.services`, lo que les da métodos básicos como `obtener()`, `crear()`, etc.

### 3.3. Controladores (ViewSets)
Los ViewSets (`_views.py`) se encargan exclusivamente de:
1. Validar la entrada (request).
2. Llamar a la capa de Servicios.
3. Formatear la salida (Response).
4. Manejar permisos y roles.

## 4. Cómo Crear un Nuevo Módulo

Supongamos que queremos crear un submódulo para "Inventarios Avanzados" (Lotes, Proveedores) dentro de `negocio`.

1. **Crear la carpeta**:
   `mkdir -p apps/negocio/inventario/api`
   `mkdir -p apps/negocio/inventario/services`

2. **Crear el Modelo (`models.py`)**:
   Definiríamos `Proveedor` o `Lote` en `apps/negocio/models.py` (o en su propio `models.py` dentro del submódulo, dependiendo de cuán acoplado esté).

3. **Crear el Serializer (`serializers.py`)**:
   ```python
   # apps/negocio/inventario/api/serializers.py
   from rest_framework import serializers
   from apps.negocio.models import Proveedor
   
   class ProveedorSerializer(serializers.ModelSerializer):
       class Meta:
           model = Proveedor
           fields = '__all__'
   ```

4. **Crear el Servicio (`proveedor_service.py`)**:
   ```python
   # apps/negocio/inventario/services/proveedor_service.py
   from apps.core.services import BaseService
   from apps.negocio.models import Proveedor
   
   class ProveedorService(BaseService):
       def __init__(self):
           super().__init__(Proveedor)
       
       def logic_especial_de_proveedor(self):
           pass
   ```

5. **Crear el ViewSet (`views.py`)**:
   ```python
   # apps/negocio/inventario/api/views.py
   from rest_framework import viewsets
   from apps.core.views import BaseViewSet
   
   class ProveedorViewSet(BaseViewSet):
       queryset = Proveedor.objects.all()
       serializer_class = ProveedorSerializer
       # ...
   ```

6. **Registrar las Rutas en `config/urls.py`**:
   ```python
   # config/urls.py
   from apps.negocio.inventario.api.views import ProveedorViewSet
   router.register(r'proveedores', ProveedorViewSet, basename='proveedores')
   ```

## 5. Autenticación y Multi-Tenancy

- **django-tenants**: Cada solicitud entra por el middleware y asigna `connection.schema_name` basado en el subdominio (ej. `sony.miproyecto.com`). Si es `miproyecto.com`, va al esquema `public`.
- **JWT de Vendedores (UsuarioJWTAuthentication)**: Usuarios internos (vendedores, admins) que gestionan el tenant.
- **JWT de Clientes (ClienteJWTAuthentication)**: Compradores de la tienda. Tienen un token más liviano (`ClienteTokenUser`) con `role="CLIENTE"`.

**Regla Importante**: Siempre verifica los permisos en el ViewSet. Usa `user_role = getattr(request.user, 'role', getattr(request.user, 'rol', None))` para saber si es un CLIENTE, VENDEDOR, o ADMIN.
