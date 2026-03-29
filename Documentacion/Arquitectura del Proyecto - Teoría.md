Este documento detalla la arquitectura del sistema, explicando cómo se comunican las diferentes capas, el propósito de cada librería utilizada y la estructura de carpetas del proyecto.

El sistema sigue una arquitectura **Desacoplada (Decoupled Architecture)**, donde el Frontend (React) y el Backend (Django) son aplicaciones completamente independientes que se comunican exclusivamente mediante una **API REST** usando formato JSON.
![[Pasted image 20260329000228.png]] ![[Pasted image 20260329000259.png]]

## 1. Arquitectura del Backend (Django + API REST)

En lugar de que el servidor devuelva vistas HTML (como lo haría Blade en Laravel), Django actúa puramente como un proveedor de datos (API).

### 🔄 ¿Cómo funciona el flujo Django + API REST?

1. **La Petición:** React envía una petición HTTP (ej. `GET /api/productos/`) incluyendo el JWT y el subdominio (`cliente1.localhost`).
    
2. **El Middleware (Tenant):** `django-tenants` intercepta la petición, lee el subdominio y cambia automáticamente la conexión de PostgreSQL al esquema de ese cliente específico.
    
3. **El Enrutador (`urls.py`):** Dirige la petición al controlador adecuado (ViewSet). _(Equivalente a `routes/api.php` en Laravel)_.
    
4. **El Controlador (`views.py`):** Recibe la petición, verifica los permisos y pide los datos a la base de datos a través del Modelo (`models.py`). _(Equivalente a los Controllers y Eloquent en Laravel)_.
    
5. **El Serializador (`serializers.py`):** Toma los objetos complejos de Python/Base de datos y los traduce a formato JSON para que React los pueda leer. _(Equivalente a los API Resources en Laravel)_.
    

### 📚 Librerías del Backend

|   |   |   |
|---|---|---|
|**Librería**|**Propósito en el Proyecto**|**Equivalencia en Laravel / PHP**|
|**Django**|Framework Web base (ORM, enrutamiento, seguridad).|Laravel Framework|
|**django-tenants**|Gestiona el aislamiento de datos (Multi-tenancy). Crea un esquema separado en PostgreSQL por cliente.|Paquetes como `tenancy/tenancy` o `spatie/laravel-multitenancy`|
|**Django REST Framework (DRF)**|Construcción de la API. Facilita la creación de ViewSets y Serializadores.|N/A (Laravel lo trae nativo)|
|**djangorestframework-simplejwt**|Genera y valida los JSON Web Tokens (JWT) para mantener la sesión abierta sin estado.|Laravel Passport o Sanctum|
|**django-cors-headers**|Reglas de seguridad CORS. Permite que el puerto 3000 (React) hable con el puerto 8000 (Django).|Middleware de CORS en Laravel|
|**psycopg2-binary**|Driver oficial para que Python pueda conectarse a PostgreSQL.|PDO_PGSQL|

### 📁 Estructura de Carpetas del Backend

Basado en el directorio del servidor:

- 📂 **`config/`** _(El cerebro del proyecto)_
    
    - Esta es la carpeta principal de configuración de Django.
        
    - `settings.py`: Contiene las variables globales, conexión a BD, configuración de apps (Shared vs Tenant) y JWT. _(Como `config/` y `.env` en Laravel)_.
        
    - `urls.py`: El mapa maestro de rutas de toda la API.
        
- 📂 **`customers/`** _(App Compartida / Shared App)_
    
    - Contiene la lógica global del SaaS. Todo lo que vive aquí se guarda en el esquema `public` de la BD.
        
    - Maneja los modelos **Client** (Inquilinos), **Domain** (Subdominios de los inquilinos) y **Usuario** (Cuentas globales con acceso al sistema).
        
- 📂 **`app_negocio/`** _(App del Inquilino / Tenant App)_
    
    - Contiene la lógica exclusiva del negocio de cada cliente. Lo que vive aquí se guarda en esquemas separados (`cliente1`, `cliente2`).
        
    - `models.py`: Define cómo se guardan los productos en BD.
        
    - `serializers.py`: Define cómo se empaquetan los productos en JSON.
        
    - `views.py`: Los endpoints (CRUD) para gestionar los productos.
        

## 2. Arquitectura del Frontend (React)

El Frontend es una **Single Page Application (SPA)**. Esto significa que la página web se carga una sola vez y, a medida que el usuario navega, React solo actualiza las partes necesarias de la pantalla solicitando datos al Backend por detrás.

### 🔄 ¿Cómo funciona el flujo en React?

1. **Rutas (React Router):** Lee la URL del navegador y decide qué componente mostrar (Pantalla Login o Pantalla Dashboard).
    
2. **Estado (State):** El componente carga y declara un estado vacío (ej. `productos = []`).
    
3. **Efecto (useEffect):** Al cargar la pantalla, dispara una petición asíncrona usando **Axios** hacia el Backend.
    
4. **Renderizado:** Cuando Axios recibe el JSON con los datos, actualiza el estado (`setProductos`) y React redibuja automáticamente la tabla en la pantalla.
    

### 📚 Librerías del Frontend

|   |   |
|---|---|
|**Librería**|**Propósito en el Proyecto**|
|**React**|Biblioteca core para construir la interfaz mediante componentes reutilizables.|
|**React Router DOM**|Maneja la navegación en el cliente. Permite proteger rutas privadas (ej. el Dashboard) y enviar parámetros por la URL para el SSO.|
|**Axios**|Cliente HTTP. Hace el trabajo sucio de enviar peticiones (GET/POST) a Django. Usamos sus _Interceptors_ para inyectar automáticamente el JWT en cada llamada.|
|**Lucide React**|Proporciona los iconos vectoriales limpios y modernos utilizados en la interfaz (ej. iconos de carrito, salir, gráficas).|
|**Tailwind CSS**|Framework de CSS que permite estilizar la aplicación rápidamente mediante clases utilitarias directamente en el código de React.|

### 📁 Estructura de Carpetas del Frontend

Basado en el directorio `/frontend`:

- 📂 **`node_modules/`**: Las dependencias instaladas vía npm. _(Equivalente a la carpeta `vendor/` de Composer)_.
    
- 📂 **`public/`**: Archivos estáticos públicos que no pasan por el compilador (favicon, `index.html` base).
    
- 📂 **`src/`** _(El código fuente de tu aplicación)_
    
    - `App.js`: El archivo raíz. Aquí configuramos el enrutador (`<Router>`), definimos el "Guardia de Seguridad" (`PrivateRoute`) y la "Aduana" para atrapar los tokens del Single Sign-On.
        
    - `index.js`: El punto de entrada que "monta" tu App.js dentro del HTML.
        
- 📂 **`src/components/`** _(Tus legos visuales)_
    
    - `Login.js`: Pantalla que captura credenciales y ejecuta el salto entre dominios.
        
    - `Dashboard.js`: Pantalla protegida que consume la API de productos y dibuja los gráficos y la tabla.
        
- 📂 **`src/services/`** _(La capa de comunicación)_
    
    - `api.js`: La configuración maestra de Axios. Aquí se define la `baseURL` dinámica para apuntar siempre al subdominio correcto, y se intercepta cada petición para pegarle el Token de seguridad.
        
- 📂 **`src/contexts/`** _(Estado global)_
    
    - _Ej: TenantContext._ Archivos que permiten guardar información general (como el nombre de la tienda actual) para que cualquier componente pueda acceder a ella sin tener que pasarla de padre a hijo constantemente.