# Conceptos Clave - Glosario Técnico

Referencia rápida de términos utilizados en la arquitectura del sistema.

---

## A

### API (Application Programming Interface)
Interfaz que permite que diferentes aplicaciones se comuniquen entre sí. En este proyecto, la **API REST** permite que el frontend se comunique con el backend mediante peticiones HTTP (GET, POST, PUT, DELETE).

**Ejemplo:** `GET /api/productos/` devuelve un listado de productos en JSON.

---

### Auditoría (Bitácora)
Sistema de registro de todas las acciones realizadas en el sistema (crear, editar, eliminar, login, etc.). 

**¿Por qué?** Para cumplir regulaciones, detectar problemas y auditar quién hizo qué y cuándo.

**En el proyecto:** `BitacoraService` registra automáticamente mediante `AuditoriaMixin`.

---

## B

### BaseService
Clase base que proporciona CRUD genérico (crear, obtener, actualizar, eliminar) a todos los servicios.

```python
class UsuarioService(BaseService):
    def __init__(self):
        super().__init__(Usuario)  # ✅ Hereda CRUD automático
```

**Beneficio:** No repites código CRUD en cada servicio.

---

### BaseViewSet
Clase base que hereda de `MultiTenantMixin`, `AuditoriaMixin` y `ModelViewSet`.

```python
class ProductoViewSet(BaseViewSet):  # ✅ Multi-tenant + Auditoría automáticos
    queryset = Producto.objects.all()
```

---

### BitacoraService
Servicio que registra todas las acciones en la tabla `Bitacora`. Captura:
- Usuario que realizó la acción
- Módulo afectado (Usuario, Producto, etc.)
- Tipo de acción (CREAR, EDITAR, ELIMINAR, LOGIN)
- IP y navegador
- Metadatos (ID del objeto, cambios realizados)

---

## C

### CORS (Cross-Origin Resource Sharing)
Mecanismo que permite que una aplicación en un dominio (frontend: puerto 3000) acceda a recursos en otro dominio (backend: puerto 8000).

**Sin CORS:** El navegador bloquea la petición por seguridad.

**En el proyecto:** Configurado en `settings.py` con `CORS_ALLOW_ALL_ORIGINS = True` (desarrollo).

---

### CRUD
Operaciones básicas sobre datos:
- **C**reate (crear)
- **R**ead (leer)
- **U**pdate (actualizar)
- **D**elete (eliminar)

**Equivalente HTTP:**
- CREATE → POST
- READ → GET
- UPDATE → PUT
- DELETE → DELETE

---

## D

### Django
Framework web Python para construir aplicaciones web rápidamente con ORM (Object-Relational Mapping) integrado.

**En el proyecto:** Django 6.0.3 + Django REST Framework para APIs.

---

### Django REST Framework (DRF)
Librería que extiende Django para construir APIs REST con serializers, viewsets y autenticación integrada.

**¿Qué ofrece?**
- Serializers (convertir modelos a JSON)
- ViewSets (vistas con CRUD automático)
- Autenticación y permisos

---

### django-tenants
Librería que implementa **multi-tenancy** mediante esquemas PostgreSQL.

**¿Cómo funciona?**
1. Cada cliente = un esquema PostgreSQL separado
2. Middleware intercepta el dominio y conecta al schema correcto
3. Todas las queries se filtran automáticamente por schema

**Beneficio:** Aislamiento de datos garantizado.

---

### Domain (Dominio)
Nombre de dominio asociado a un cliente en un sistema multi-tenant.

**Ejemplo:** 
- `cliente1.localhost` → Schema `cliente1`
- `cliente2.localhost` → Schema `cliente2`
- `admin.localhost` → Schema `public`

**En el proyecto:** Tabla `Domain` vincula dominios a clientes.

---

## E

### Esquema (Schema)
En PostgreSQL, contenedor lógico de tablas. Similar a una base de datos dentro de la BD.

**Esquemas en el proyecto:**
- `public` → Datos compartidos (clientes, dominios, usuarios)
- `cliente1` → Datos de cliente 1 (productos, ventas)
- `cliente2` → Datos de cliente 2 (productos, ventas)

**Aislamiento:** Query en schema `cliente1` NO ve datos de `cliente2`.

---

## F

### FK (Foreign Key)
Relación entre dos tablas. Ejemplo: `Usuario` tiene FK a `Client`.

```python
class Usuario(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
```

**¿Por qué?** Usuario vive en schema público (compartido), pero pertenece a un cliente específico.

---

## J

### JWT (JSON Web Token)
Estándar para autenticación sin estado. El servidor genera un token, el cliente lo envía en cada petición, el servidor lo valida.

**Estructura:** `header.payload.signature`

**Ejemplo:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**En el proyecto:** `djangorestframework-simplejwt` genera y valida tokens.

**Ventaja:** Escalable (sin sesiones en servidor).

---

## M

### Middleware
Interceptor de peticiones que se ejecuta antes de llegar a la vista.

**Ejemplo en el proyecto:** `django-tenants` tiene middleware que:
1. Lee el Host de la petición
2. Encuentra el schema correspondiente
3. Conecta a ese schema
4. Todas las queries se filtran automáticamente

---

### Mixin
Clase pequeña que "inyecta" funcionalidad reutilizable en otras clases.

**Analogía:** Es como un "ingrediente" que puedes mezclar en múltiples "recetas".

```python
class AuditoriaMixin:
    def perform_create(self, serializer):
        # Auditoría automática
        
class ProductoViewSet(AuditoriaMixin, ModelViewSet):
    # ✅ Hereda auditoría
```

**Beneficio:** Cero duplication, máxima reutilización.

---

### Multi-tenancy (Multi-tenant)
Arquitectura donde múltiples clientes comparten la misma aplicación pero con datos aislados.

**Tipos:**
1. **Database-level:** Cada cliente tiene su BD
2. **Schema-level:** Cada cliente tiene su esquema (nuestro proyecto ✅)
3. **Row-level:** Todos usan la misma tabla pero filtrada por cliente_id

**Ventaja:** Costo bajo, escalabilidad, mantenimiento centralizado.

---

## O

### ORM (Object-Relational Mapping)
Librería que convierte filas de BD en objetos Python.

**Sin ORM:**
```sql
SELECT * FROM usuarios WHERE email = 'algo@mail.com';
```

**Con ORM (Django):**
```python
Usuario.objects.get(email='algo@mail.com')  # ✅ Más Python, menos SQL
```

**En el proyecto:** Django ORM + `django-tenants`.

---

## P

### PostgreSQL
Base de datos relacional open-source. Soporta esquemas nativamente.

**¿Por qué?** Multi-tenant schema-based requiere esquemas de BD.

---

### Producto
Entidad de negocio que representa un artículo en el catálogo.

**Modelos:**
```python
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
```

**¿Dónde vive?** En el schema del cliente (NO en public).

---

## Q

### QuerySet
Objeto de Django que representa una consulta a la BD (lazy evaluation).

```python
productos = Producto.objects.all()  # ✅ No ejecuta query aún
for producto in productos:          # ✅ Aquí sí ejecuta
    print(producto.nombre)
```

**MultiTenantMixin override `get_queryset()`** para filtrar automáticamente.

---

## R

### REST (Representational State Transfer)
Arquitectura para APIs que usa HTTP como protocolo.

**Principios:**
- Recursos identificados por URLs (`/api/productos/`)
- Operaciones por métodos HTTP (GET, POST, PUT, DELETE)
- Sin estado (stateless)

**Ejemplo:**
- `GET /api/productos/1/` → Lee producto 1
- `POST /api/productos/` → Crea nuevo producto
- `PUT /api/productos/1/` → Actualiza producto 1
- `DELETE /api/productos/1/` → Elimina producto 1

---

### RESTful API
API que sigue los principios REST (nuestro proyecto ✅).

---

## S

### Schema (ver Esquema)

### Serializer
Objeto de Django REST Framework que:
1. Convierte modelos a JSON (serialización)
2. Convierte JSON a modelos (deserialización)
3. Valida datos

```python
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio']  # ✅ Explícito
```

---

### Service
Clase que contiene lógica de negocio (no se puede poner en modelos ni views).

```python
class ProductoService(BaseService):
    def rebajar_stock(self, producto, cantidad):
        if producto.stock < cantidad:
            raise ValueError("Stock insuficiente")
        producto.stock -= cantidad
        producto.save()
        return producto
```

**Regla:** Si es lógica de negocio, va en Service.

---

## T

### Tenant
Cliente de la aplicación SaaS (Software as a Service).

**Ejemplo:**
- Tenant 1: "Tienda ABC"
- Tenant 2: "Tienda XYZ"

**Cada tenant:**
- Tiene su schema PostgreSQL
- Sus propios productos, usuarios, pedidos
- No ve datos de otros tenants

---

### Transacción
Operación atómica: se ejecuta todo o nada.

```python
@transaction.atomic
def crear_producto_con_auditoria(self, datos):
    producto = Producto.objects.create(**datos)
    BitacoraService.registrar_accion(...)
    # Si algo falla aquí, ambas operaciones se revierten
```

**Beneficio:** Consistencia de datos.

---

## U

### Usuario
Entidad que representa una persona en el sistema.

```python
class Usuario(models.Model):
    email = models.EmailField(unique=True)
    client = models.ForeignKey(Client)  # FK a Cliente
```

**¿Dónde vive?** En schema `public` (compartido), pero vinculado a un cliente.

**¿Por qué?** Permite SSO (Single Sign-On) y un usuario acceder a múltiples clientes.

---

## V

### ViewSet
Objeto de Django REST Framework que genera CRUD automático.

```python
class ProductoViewSet(BaseViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    # ✅ Automáticamente: GET /api/productos/ (listar)
    #    GET /api/productos/1/ (detalle)
    #    POST /api/productos/ (crear)
    #    PUT /api/productos/1/ (actualizar)
    #    DELETE /api/productos/1/ (eliminar)
```

---

## Z

### Zero-Downtime Deployment
Estrategia de despliegue sin parar el servidor. Nuestro arquitectura lo soporta:
- Cambios en Services → Solo editar lógica
- Cambios en Schemas → django-tenants maneja migración gradual
- Cambios en APIs → Versionado de endpoints

---

## REFERENCIAS RÁPIDAS

**Por Tema:**

**Multi-tenancy:**
- Schema-based Multi-tenancy
- django-tenants
- Domain
- Tenant

**Backend:**
- Django
- Django REST Framework
- ORM
- ViewSet
- Serializer
- Service
- Mixin
- BaseService
- BaseViewSet

**Seguridad:**
- JWT
- Auditoría
- CORS
- Transacción

**BD:**
- PostgreSQL
- Esquema
- QuerySet
- FK

**Arquitectura:**
- REST
- API
- CRUD
- Middleware

---

**Última actualización:** 21 de Abril, 2026  
**Estado:** Glosario técnico completo ✅
