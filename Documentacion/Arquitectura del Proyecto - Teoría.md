# Arquitectura del Sistema (Clean Architecture / Monolito Modular)

Este documento detalla la arquitectura del sistema, explicando cómo se comunican las diferentes capas, el propósito de cada librería utilizada y la estructura de carpetas del proyecto.

El sistema sigue una arquitectura **Desacoplada (Decoupled Architecture)**, donde el Frontend (React) y el Backend (Django) son aplicaciones completamente independientes que se comunican exclusivamente mediante una **API REST** usando formato JSON. 

En el Backend, aplicamos los principios de **Clean Architecture** (arquitectura por capas) para separar las responsabilidades de infraestructura, validación y lógica de negocio.

<img width="1536" height="1024" alt="Flujo de datos Django" src="https://github.com/user-attachments/assets/1d783a2e-1842-46e9-92a3-af49d49a5bbd" />
<img width="2752" height="1536" alt="unnamed (1)" src="https://github.com/user-attachments/assets/c75456eb-2762-493e-a3b4-3396b03f4139" />
<img width="2752" height="1536" alt="unnamed (2)" src="https://github.com/user-attachments/assets/17bd9b49-2c1b-44ed-a1d1-00fcd2854c83" />

---

## 1. Arquitectura del Backend (Django + API REST)

Django no devuelve vistas HTML (como lo haría Blade en Laravel), sino que actúa puramente como un motor de lógica y proveedor de datos (API).

### 🧠 El Corazón de la Arquitectura: Vistas, Serializadores y Servicios

Para que el sistema sea escalable y fácil de mantener, el procesamiento de cada petición se divide en cuatro actores principales:

1.  **La Vista (El Orquestador):**
    * **Función:** Es la puerta de entrada. Su único trabajo es recibir la petición HTTP, llamar al Serializador para validar los datos, delegar al Servicio para ejecutar la lógica de negocio y, finalmente, devolver la respuesta HTTP (200 OK, 400 Bad Request).
    * **Herencia:** Todos heredan de `BaseViewSet` que incluye **Mixins** para auditoría y multi-tenant automáticos.
    * **Regla:** *No contiene lógica compleja ni hace consultas directas a la base de datos.*
2.  **El Serializador (El Traductor y Filtro):**
    * **Función:** Convierte los objetos complejos de la Base de Datos a JSON (para que React los entienda) y viceversa. Además, es la "Aduana": valida que los datos que entran tengan el formato correcto (ej. que un email sea realmente un email, o que un precio sea un número positivo).
    * **Regla:** *No toma decisiones de negocio (ej. no decide si aplicar un descuento o enviar un correo).*
3.  **El Servicio (El Cerebro / Lógica de Negocio):**
    * **Función:** Aquí vive la inteligencia del sistema. Son funciones puras de Python que hacen el trabajo pesado: calculan inventarios, crean registros, asignan permisos o envían notificaciones.
    * **Herencia:** Heredan de `BaseService` que proporciona CRUD genérico con transacciones automáticas.
    * **Regla:** *No saben qué es un JSON ni una petición HTTP. Solo reciben datos limpios, ejecutan reglas del negocio y devuelven un resultado a la Vista.*
4.  **Los Mixins (Reutilización de Lógica):**
    * **Función:** Clases que inyectan funcionalidad común (auditoría, filtrado multi-tenant) en las Vistas sin necesidad de código duplicado.
    * **Tipos:** `MultiTenantMixin` (filtra datos por esquema), `AuditoriaMixin` (registra acciones automáticamente).
    * **Regla:** *Una sola vez de lógica = aplicado a todos los CRUDs automáticamente.*

### 🔄 ¿Cómo funciona el flujo de una petición ahora?

1. **La Petición:** React envía una petición HTTP (ej. `POST /api/productos/`) incluyendo el JWT y el subdominio (`cliente1.localhost`).
2. **El Middleware (Tenant):** `django-tenants` intercepta la petición, lee el subdominio y enruta la conexión de PostgreSQL al esquema de ese cliente específico.
3. **El Enrutador (`urls.py`):** Dirige la petición a la **Vista** adecuada.
4. **La Vista (`views/`):** Recibe la petición y le pasa los datos crudos al **Serializador**.
5. **El Serializador (`serializers/`):** Valida que la estructura del JSON sea correcta y devuelve los datos limpios a la Vista.
6. **El Servicio (`services/`):** La Vista llama al Servicio enviándole los datos limpios. El Servicio aplica la lógica de negocio (ej. validar si hay espacio en el almacén) y guarda en la Base de Datos a través de los **Modelos (`models/`)**.
7. **La Respuesta:** El Servicio devuelve el objeto creado a la Vista, el Serializador lo traduce a JSON, y la Vista responde a React.

### 📚 Librerías del Backend

| **Librería** | **Propósito en el Proyecto** | **Equivalencia en Laravel / PHP** |
| :--- | :--- | :--- |
| **Django** | Framework Web base (ORM, enrutamiento, seguridad). | Laravel Framework |
| **django-tenants** | Gestiona el aislamiento de datos (Multi-tenancy). Crea un esquema separado en PostgreSQL por cliente. | `tenancy/tenancy` o `spatie/laravel-multitenancy` |
| **DRF** | Django REST Framework. Construcción de la API (ViewSets, Serializers). | N/A (Laravel lo trae nativo) |
| **simplejwt** | Genera y valida los JSON Web Tokens (JWT) para sesiones seguras. | Laravel Passport o Sanctum |
| **cors-headers** | Reglas CORS. Permite que React (puerto 3000) hable con Django (puerto 8000). | Middleware de CORS en Laravel |
| **psycopg2** | Driver oficial para que Python interactúe con PostgreSQL. | PDO_PGSQL |

### 📁 Estructura de Carpetas del Backend (Modular)

Basado en el directorio del servidor, el código se divide en paquetes funcionales:

* 📂 **`config/`** *(El cerebro del proyecto)*
    * `settings.py`: Variables globales, conexión a BD, configuración de apps (Shared vs Tenant).
    * `urls.py`: El mapa maestro de rutas globales.
* 📂 **`core/`** *(Infraestructura Compartida - NUEVO)*
    * `mixins.py`: `MultiTenantMixin` y `AuditoriaMixin` reutilizables.
    * `views.py`: `BaseViewSet` que hereda de ambos Mixins.
    * `services.py`: `BaseService` con CRUD genérico y transacciones automáticas.
    * `validators.py`: Validadores centralizados por dominio.
    * `exceptions.py`: Excepciones personalizadas del negocio.
* 📂 **`customers/`** *(App Compartida - Esquema Público)*
    * Contiene la lógica global del SaaS y la gestión de la infraestructura (Inquilinos y Dominios).
* 📂 **`app_negocio/`** *(App del Inquilino - Esquemas Aislados)*
    * Contiene la lógica exclusiva del negocio (Productos, Ventas).
    * *Internamente, ambas apps siguen esta estructura modular:*
        * 📁 `models/`: Archivos separados por entidad (ej. `producto.py`, `categoria.py`) que definen las tablas de la BD.
        * 📁 `views/`: Los orquestadores HTTP (ViewSets que heredan de `BaseViewSet`).
        * 📁 `serializers/`: Los traductores de JSON (ej. `producto_serializers.py`).
        * 📁 `services/`: Las reglas de negocio (heredan de `BaseService`).
        * 📁 `admin/`: Configuración de seguridad e interfaz del panel administrativo (`TenantSafeAdmin`).
        * 📄 `__init__.py`: Archivos índice que mantienen las importaciones limpias y centralizadas en todo el sistema.

---

## 2. Arquitectura del Frontend (React)

El Frontend es una **Single Page Application (SPA)**. La web carga una sola vez y React solo actualiza las partes necesarias solicitando datos al Backend por detrás.

### 🔄 ¿Cómo funciona el flujo en React?

1. **Rutas (React Router):** Lee la URL y decide qué componente mostrar.
2. **Estado (State):** El componente carga y declara un estado vacío (`productos = []`).
3. **Efecto (useEffect):** Al montar la pantalla, dispara una petición asíncrona vía **Axios** hacia el Backend.
4. **Renderizado:** Al recibir el JSON, actualiza el estado (`setProductos`) y React redibuja automáticamente la interfaz.

### 📚 Librerías del Frontend

| **Librería** | **Propósito en el Proyecto** |
| :--- | :--- |
| **React** | Biblioteca core para construir la interfaz mediante componentes. |
| **React Router DOM** | Maneja la navegación en el cliente, protección de rutas y envío de parámetros URL para el SSO. |
| **Axios** | Cliente HTTP. Usamos sus *Interceptors* para inyectar automáticamente el JWT y dirigir peticiones al subdominio correcto. |
| **Lucide React** | Iconografía vectorial moderna. |
| **Tailwind CSS** | Framework de CSS utilitario para estilizado rápido y responsivo. |

### 📁 Estructura de Carpetas del Frontend

Basado en el directorio `/frontend`:

* 📂 **`node_modules/`**: Dependencias npm (equivalente a `vendor/` de Composer).
* 📂 **`public/`**: Archivos estáticos (`index.html`, favicon).
* 📂 **`src/`** *(Código fuente)*
    * `App.js`: Archivo raíz, configuración de enrutador y guardias de seguridad (`PrivateRoute`).
    * 📁 `components/`: "Legos visuales" (Pantallas como `Login.js`, `Dashboard.jsx`).
    * 📁 `services/`: Capa de comunicación (`api.js` maestro de Axios).
    * 📁 `contexts/`: Estado global (ej. `TenantContext.js`) para compartir datos generales sin "prop drilling".
