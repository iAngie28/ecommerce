# CRUDs Implementados

Este documento describe la implementación completa de los servicios REST del sistema de ecommerce, siguiendo la arquitectura de capas (Models → Services → Serializers → ViewSets → URLs).

El sistema cuenta con 9 CRUDs funcionales que cubren la infraestructura del SaaS (gestión de roles, planes y clientes) y la lógica de negocio (categorías, carritos, pedidos y facturas).

---

## 1. Estructura General de los CRUDs

Cada CRUD sigue el patrón de cuatro capas establecido en la arquitectura:

1. **Modelo (Models):** Define la estructura de datos en PostgreSQL.
2. **Servicio (Service):** Contiene la lógica de negocio con transacciones atómicas.
3. **Serializador (Serializer):** Valida datos de entrada y serializa respuestas JSON.
4. **Vista (ViewSet):** Orquesta las peticiones HTTP usando el Serializador y el Servicio.

La separación en capas garantiza que cada CRUD es testeable, reutilizable y fácil de mantener.

---

## 2. CRUDs de Infraestructura (customers app)

### 2.1 Rol

Gestiona los permisos y niveles de acceso de los usuarios administrativos del sistema.

**Endpoints:**
```
GET    /api/roles/             Listar todos
POST   /api/roles/             Crear
GET    /api/roles/{id}/        Detalle
PUT    /api/roles/{id}/        Actualizar
DELETE /api/roles/{id}/        Eliminar
PATCH  /api/roles/{id}/        Actualización parcial
```

**Modelos de datos:**
- `nombre` (CharField, único): Nombre del rol (ej. ADMIN, VENDEDOR).
- `descripcion` (TextField): Descripción de responsabilidades.
- `nivel` (IntegerField): Jerarquía numérica (1=ADMIN, 2=VENDEDOR, 3=CLIENTE, 4=VIEWER).
- `activo` (BooleanField): Indica si el rol puede ser asignado.

**Características:**
- Validación de unicidad en el nombre.
- Niveles predefinidos con constantes en el modelo.
- Filtrado automático de roles inactivos en listados.

---

### 2.2 Plan

Define los tipos de suscripción disponibles en el SaaS, con precios y límites de recursos.

**Endpoints:**
```
GET    /api/planes/            Listar todos
POST   /api/planes/            Crear
GET    /api/planes/{id}/       Detalle
PUT    /api/planes/{id}/       Actualizar
DELETE /api/planes/{id}/       Eliminar
PATCH  /api/planes/{id}/       Actualización parcial
```

**Modelos de datos:**
- `nombre` (CharField, único): Ej. Plan Básico, Plan Profesional.
- `descripcion` (TextField): Características incluidas.
- `precio_mensual` (DecimalField): Costo mensual en USD.
- `precio_anual` (DecimalField): Costo anual con descuento.
- `max_usuarios` (IntegerField): Límite de usuarios administrativos.
- `max_productos` (IntegerField): Cantidad máxima de productos en catálogo.
- `facturacion_max` (DecimalField): Límite de ingresos mensuales permitidos.
- `activo` (BooleanField): Indica si está disponible para nuevas suscripciones.

**Características:**
- Los precios se almacenan en una única moneda (USD).
- Cada plan tiene límites de escalabilidad específicos.
- Se referencia desde el modelo `Client` para tracking de SaaS.

---

### 2.3 Cliente

Representa clientes públicos que realizan compras en la plataforma (diferentes de `Usuario` que son administrativos).

**Endpoints:**
```
GET    /api/clientes/          Listar todos
POST   /api/clientes/          Crear (encripta contraseña)
GET    /api/clientes/{id}/     Detalle
PUT    /api/clientes/{id}/     Actualizar
DELETE /api/clientes/{id}/     Eliminar
PATCH  /api/clientes/{id}/     Actualización parcial
```

**Modelos de datos:**
- `nombre` (CharField): Nombre del cliente.
- `correo` (EmailField, único): Correo para login y notificaciones.
- `telefono` (CharField): Contacto primario.
- `contrasena` (CharField): Contraseña encriptada con PBKDF2.
- `nit` (CharField): Número de identificación tributaria (Bolivia).
- `fecha_registro` (DateTimeField): Timestamp automático.
- `activo` (BooleanField): Indica si puede realizar compras.

**Características:**
- Las contraseñas se encriptan automáticamente mediante `set_password()`.
- El correo es único a nivel global (válido para múltiples tenants).
- Cada cliente puede tener múltiples carritos.
- La auditoría registra cambios de estado (activación/desactivación).

---

## 3. CRUDs de Negocio (app_negocio)

### 3.1 Categoría

Organiza el catálogo de productos con soporte para subcategorías mediante relación jerárquica.

**Endpoints:**
```
GET    /api/categorias/        Listar todos
POST   /api/categorias/        Crear
GET    /api/categorias/{id}/   Detalle (incluye ruta completa)
PUT    /api/categorias/{id}/   Actualizar
DELETE /api/categorias/{id}/   Eliminar
PATCH  /api/categorias/{id}/   Actualización parcial
```

**Modelos de datos:**
- `nombre` (CharField): Nombre de la categoría.
- `descripcion` (TextField): Descripción del contenido.
- `parent` (ForeignKey a self): Referencia a categoría padre para subcategorías.
- `activo` (BooleanField): Filtro para listados.
- `fecha_creacion` (DateTimeField): Timestamp automático.

**Características:**
- Estructura de árbol: una categoría puede contener otras categorías.
- Propiedad `ruta_completa` que retorna la jerarquía completa (ej. "Electrónica > Smartphones > Android").
- Validación: una categoría no puede ser subcategoría de sí misma.
- Se referencia desde `Producto` para clasificación.

---

### 3.2 Carrito

Gestiona carritos de compra con validación de stock y cálculos automáticos.

**Endpoints:**
```
GET    /api/carritos/          Listar todos
POST   /api/carritos/          Crear nuevo carrito
GET    /api/carritos/{id}/     Detalle (incluye items nested)
PUT    /api/carritos/{id}/     Actualizar estado
DELETE /api/carritos/{id}/     Eliminar (cascada)
PATCH  /api/carritos/{id}/     Actualización parcial

POST   /api/carritos/{id}/agregar-item/      Agregar producto
POST   /api/carritos/{id}/eliminar-item/     Remover producto
POST   /api/carritos/{id}/vaciar/            Limpiar todos los items
POST   /api/carritos/{id}/cerrar/            Convertir en pedido
```

**Modelos de datos:**
- `cliente` (ForeignKey): Referencia a Cliente.
- `estado` (CharField): ABIERTO, CERRADO, ABANDONADO.
- `fecha_creacion` (DateTimeField): Automático.
- `fecha_actualizacion` (DateTimeField): Se actualiza en cada cambio.

**Características:**
- Cálculos automáticos:
  - `cantidad_items` (propiedad): Suma de cantidades de todos los items.
  - `total_carrito` (propiedad): Suma de subtotales (precio * cantidad).
- Validaciones:
  - No se puede agregar producto si el stock es insuficiente.
  - No se puede agregar a un carrito CERRADO.
  - No se puede cerrar un carrito vacío.
- Operaciones especiales:
  - Al agregar un producto que ya existe, se incrementa la cantidad (no crea duplicado).
  - Vaciar carrito elimina todos los items sin eliminar el carrito.
  - Cerrar carrito cambia estado a CERRADO y prepara para crear pedido.

---

### 3.3 CarritoItem

Representa cada producto en el carrito con cantidad y cálculo de subtotal.

**Modelos de datos:**
- `carrito` (ForeignKey): Referencia al Carrito.
- `producto` (ForeignKey): Referencia al Producto.
- `cantidad` (IntegerField): Número de unidades.
- `fecha_agregado` (DateTimeField): Automático.
- Restricción única: No se pueden duplicar (carrito, producto).

**Características:**
- Propiedad `subtotal`: Calcula `producto.precio * cantidad`.
- No tiene ViewSet propio (se gestiona via CarritoViewSet).
- Se serializa anidado en la respuesta de Carrito.

---

### 3.4 Pedido

Ordenes creadas a partir de carritos con seguimiento de estados.

**Endpoints:**
```
GET    /api/pedidos/           Listar todos
POST   /api/pedidos/           Crear
GET    /api/pedidos/{id}/      Detalle
PUT    /api/pedidos/{id}/      Actualizar
DELETE /api/pedidos/{id}/      Eliminar
PATCH  /api/pedidos/{id}/      Actualización parcial

POST   /api/pedidos/crear-desde-carrito/     Generar pedido de carrito
POST   /api/pedidos/{id}/cambiar-estado/     Transicionar estado
```

**Modelos de datos:**
- `carrito` (OneToOneField): Referencia única al Carrito.
- `estado` (CharField): PENDIENTE, PROCESADO, ENVIADO, ENTREGADO, CANCELADO.
- `fecha_creacion` (DateTimeField): Automático.
- `fecha_actualizacion` (DateTimeField): Se actualiza en cambios de estado.
- `observaciones` (TextField): Notas del administrador.

**Características:**
- Relación 1:1 con Carrito: cada carrito genera máximo un pedido.
- Validaciones de transición de estado:
  - PENDIENTE puede pasar a PROCESADO o CANCELADO.
  - PROCESADO puede pasar a ENVIADO o CANCELADO.
  - ENVIADO puede pasar a ENTREGADO.
  - ENTREGADO y CANCELADO son estados finales.
- El servicio `PedidoService.crear_pedido_desde_carrito()`:
  - Valida que el carrito esté abierto y tenga items.
  - Cierra el carrito automáticamente.
  - Crea el Pedido en estado PENDIENTE.
  - Todo es atómico (una transacción).

---

### 3.5 Factura y TipoPago

Documentos legales de venta y métodos de pago.

**Endpoints (Factura):**
```
GET    /api/facturas/          Listar todas
POST   /api/facturas/          Crear
GET    /api/facturas/{nro}/    Detalle (lookup por número, no ID)
PUT    /api/facturas/{nro}/    Actualizar
DELETE /api/facturas/{nro}/    Eliminar
PATCH  /api/facturas/{nro}/    Actualización parcial

POST   /api/facturas/crear-desde-pedido/     Generar factura del pedido
POST   /api/facturas/{nro}/anular/           Anular factura (cambiar a ANULADA)
```

**Endpoints (TipoPago):**
```
GET    /api/tipos-pago/        Listar todos
POST   /api/tipos-pago/        Crear tipo
GET    /api/tipos-pago/{id}/   Detalle
PUT    /api/tipos-pago/{id}/   Actualizar
DELETE /api/tipos-pago/{id}/   Eliminar
PATCH  /api/tipos-pago/{id}/   Actualización parcial
```

**Modelos de datos (Factura):**
- `nro` (CharField): Número único en formato FAC-YYYYMMDD-XXXXX (primary_key).
- `fecha` (DateField): Automático.
- `hora` (TimeField): Automático.
- `pedido` (OneToOneField): Referencia al Pedido.
- `cliente` (ForeignKey): Referencia al Cliente (desnormalizado para auditoría).
- `tipo_pago` (ForeignKey): Referencia a TipoPago.
- `monto_total` (DecimalField): Total de la venta.
- `moneda` (CharField): Ej. USD, BOB (el sistema por defecto es USD).
- `cuf` (CharField): Código de control fiscal (Bolivia).
- `estado` (CharField): VIGENTE o ANULADA.

**Modelos de datos (TipoPago):**
- `nombre` (CharField): Ej. Efectivo, Tarjeta Crédito, Cheque.
- `descripcion` (TextField): Detalles.
- `estado` (CharField): ACTIVO o INACTIVO.

**Características:**
- El número de factura se genera automáticamente con timestamp y sufijo aleatorio.
- La creación desde pedido (`crear_factura_desde_pedido`):
  - Valida que el Pedido exista.
  - Itera sobre todos los items del carrito del pedido.
  - Crea un `DetalleFactura` por cada item.
  - Suma monto_total.
  - Crea la Factura en estado VIGENTE.
  - Todo es atómico.
- Las facturas no se pueden eliminar (solo anular, lo que es un cambio de estado).
- El lookup es por número de factura (`{nro}`) no por ID, ya que el número es el identificador público.

---

### 3.6 DetalleFactura

Líneas de artículos dentro de una factura.

**Modelos de datos:**
- `factura` (ForeignKey): Referencia a Factura.
- `producto` (ForeignKey): Referencia a Producto.
- `cantidad` (IntegerField): Unidades vendidas.
- `precio_unitario` (DecimalField): Precio en el momento de venta.
- `total` (DecimalField): Se calcula automáticamente en `save()` como `cantidad * precio_unitario`.

**Características:**
- No tiene ViewSet propio (se gestiona via FacturaViewSet).
- Se serializa anidado en la respuesta de Factura.
- Permite recuperar histórico de precios (precio_unitario congelado).
- Servicio `DetalleFacturaService` proporciona:
  - `obtener_por_factura()`: Todos los items de una factura.
  - `calcular_total_factura()`: Suma todos los totales (redundante con monto_total pero útil para validaciones).

---

## 4. Flujos de Negocio

### Flujo Principal: Compra Completa

El sistema implementa un flujo end-to-end desde registro de cliente hasta generación de factura:

1. **Registro de cliente:** 
   - POST `/api/clientes/` con nombre, correo, contraseña.
   - La contraseña se encripta automáticamente en la BD.

2. **Creación de carrito:**
   - POST `/api/carritos/` con cliente_id.
   - Estado inicial: ABIERTO.

3. **Agregar productos al carrito:**
   - POST `/api/carritos/{id}/agregar-item/` con producto_id y cantidad.
   - Validación automática: cantidad ≤ stock disponible.
   - Si el producto ya existe en el carrito, se incrementa cantidad.

4. **Crear pedido desde carrito:**
   - POST `/api/pedidos/crear-desde-carrito/` con carrito_id.
   - Validaciones:
     - Carrito debe estar ABIERTO.
     - Debe tener al menos 1 item.
   - Acciones:
     - Crear Pedido en estado PENDIENTE.
     - Cambiar carrito a estado CERRADO automáticamente.
   - Todo en una transacción atómica.

5. **Generar factura:**
   - POST `/api/facturas/crear-desde-pedido/` con pedido_id.
   - Acciones:
     - Generar número único de factura.
     - Por cada CarritoItem, crear DetalleFactura con precio congelado.
     - Calcular monto_total.
     - Crear Factura en estado VIGENTE.
   - Todo en una transacción atómica.

6. **Cambiar estado del pedido (opcional, depende del flujo del negocio):**
   - POST `/api/pedidos/{id}/cambiar-estado/` con nuevo_estado.
   - Validar transición permitida.
   - Actualizar `fecha_actualizacion`.

7. **Anular factura (si es necesario):**
   - POST `/api/facturas/{nro}/anular/`.
   - Cambiar estado a ANULADA.
   - Registrar en auditoría.

---

## 5. Características Transversales

### Automatizaciones

- **Carrito:** Cálculos de cantidad_items y total_carrito vía propiedades (no requieren actualización manual).
- **Pedido:** Cierre automático de carrito al crear desde carrito.
- **Factura:** Número único generado automáticamente. DetalleFactura generado automáticamente desde items del carrito.
- **DetalleFactura:** Cálculo automático de total = cantidad * precio_unitario en save().

### Auditoría Automática

Todos los CRUDs heredan de `AuditoriaMixin` (incluido en `BaseViewSet`), lo que registra automáticamente:
- Usuario que realizó la acción.
- Tipo de acción (CREATE, UPDATE, DELETE).
- Timestamp de la operación.
- Cambios realizados (metadatos).

No requiere código adicional en Services ni ViewSets.

### Multi-tenancy Automática

Todos los CRUDs heredan de `MultiTenantMixin` (incluido en `BaseViewSet`), lo que:
- Filtra queries por `schema_name` del tenant actual.
- Valida que el usuario no acceda a datos de otros tenants.
- Se aplica automáticamente via middleware `django-tenants`.

No requiere filtros manuales en queries.

### Transacciones Atómicas

Métodos críticos en Services están decorados con `@transaction.atomic`:
- `CarritoService.agregar_item()`: Validación + creación.
- `PedidoService.crear_pedido_desde_carrito()`: Creación de Pedido + cierre de carrito.
- `FacturaService.crear_factura_desde_pedido()`: Generación de factura + creación de detalles.

Garantiza consistencia: si falla cualquier paso, se revierte todo.

### Validaciones de Negocio

Las validaciones ocurren en la capa de Servicio (no en Serializer):
- Stock disponible antes de agregar a carrito.
- Carrito debe tener items antes de crear pedido.
- Estados de transición válidos para pedidos.
- Factura no puede anularse dos veces.

---

## 6. Estructura de Archivos

```
backend/customers/
├── models/
│   ├── rol.py                    # Definición de Rol
│   ├── plan.py                   # Definición de Plan
│   └── cliente.py                # Definición de Cliente
├── services/
│   ├── rol_service.py            # Lógica de Rol
│   ├── plan_service.py           # Lógica de Plan
│   └── cliente_service.py        # Lógica de Cliente (encriptación, activación)
├── serializers/
│   ├── rol_serializer.py         # Validación y serialización de Rol
│   ├── plan_serializer.py        # Validación y serialización de Plan
│   └── cliente_serializer.py     # Validación y serialización de Cliente
└── views/
    ├── rol_views.py              # RolViewSet (5 endpoints CRUD)
    ├── plan_views.py             # PlanViewSet (5 endpoints CRUD)
    └── cliente_views.py          # ClienteViewSet (5 endpoints CRUD)

backend/app_negocio/
├── models/
│   ├── categoria.py              # Definición de Categoría (árbol jerárquico)
│   ├── carrito.py                # Definición de Carrito
│   ├── carrito_item.py           # Definición de CarritoItem
│   ├── pedido.py                 # Definición de Pedido
│   ├── factura.py                # Definición de Factura y TipoPago
│   └── detalle_factura.py        # Definición de DetalleFactura
├── services/
│   ├── categoria_service.py      # Lógica de Categoría (jerarquía, búsqueda)
│   ├── carrito_service.py        # Lógica de Carrito (agregar, validar stock, cerrar)
│   ├── pedido_service.py         # Lógica de Pedido (crear desde carrito, transiciones)
│   ├── factura_service.py        # Lógica de Factura (generar número, crear desde pedido, anular)
│   └── detalle_factura_service.py # Lógica de DetalleFactura (agregaciones)
├── serializers/
│   ├── categoria_serializer.py   # Validación de Categoría (incluye ruta_completa)
│   ├── carrito_serializer.py     # Validación de Carrito (items nested)
│   ├── pedido_serializer.py      # Validación de Pedido (campos calculados)
│   ├── factura_serializer.py     # Validación de Factura (detalles nested, TipoPago inline)
│   └── detalle_factura_serializer.py # Validación de DetalleFactura
└── views/
    ├── categoria_views.py        # CategoriaViewSet (5 endpoints CRUD)
    ├── carrito_views.py          # CarritoViewSet (5 CRUD + 4 actions especiales)
    ├── pedido_views.py           # PedidoViewSet (5 CRUD + 2 actions especiales)
    └── factura_views.py          # FacturaViewSet (5 CRUD + 2 actions) + TipoPagoViewSet (5 CRUD)
```

---

## 7. Validaciones

| Entidad | Validación | Ubicación |
| --- | --- | --- |
| Carrito | No permitir agregar si stock < cantidad | CarritoService.agregar_item() |
| Carrito | No permitir crear pedido si está vacío | PedidoService.crear_pedido_desde_carrito() |
| Carrito | No permitir agregar a carrito CERRADO | CarritoService.agregar_item() |
| Pedido | No permitir estado inválido | PedidoService.cambiar_estado() |
| Pedido | Solo PENDIENTE→PROCESADO→ENVIADO→ENTREGADO | PedidoService.cambiar_estado() |
| Factura | No permitir anular si ya está ANULADA | FacturaService.anular_factura() |
| Cliente | Correo único global | Model constraint |
| Cliente | Contraseña encriptada | ClienteService.crear_cliente_con_contrasena() |
| Categoría | No puede ser subcategoría de sí misma | Model validación |

---

## 8. Seguridad

- **Multi-tenancy:** Cada tenant ve solo sus datos mediante filtro automático en queries.
- **Auditoría:** Todos los cambios quedan registrados con usuario, acción y timestamp.
- **Encriptación:** Contraseñas de Cliente se encriptan con PBKDF2.
- **Transacciones:** Operaciones críticas son atómicas (all-or-nothing).
- **Validaciones:** Se ejecutan en la capa de Servicio (más seguro que Serializer).

