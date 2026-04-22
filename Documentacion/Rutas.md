## 1. Acceso General (Esquema Público - localhost)

Estas rutas son el punto de entrada global a la plataforma SaaS. Aquí es donde los usuarios se autentican antes de ser derivados a sus tiendas específicas.

|   |   |   |
|---|---|---|
|**URL**|**Componente**|**Descripción**|
|`http://localhost:3000/login`|**Login Global**|Portal de acceso único. Valida credenciales y determina el subdominio del usuario.|
|`http://localhost:8000/admin/`|**Django Admin**|Gestión de base de datos global (Creación de Clientes y Dominios).|

## 2. Flujo de Sincronización (SSO)

Este es el puente técnico que permite transferir la sesión desde el dominio global hacia el subdominio privado del cliente.

|   |   |   |
|---|---|---|
|**URL Ejemplo**|**Componente**|**Acción Técnica**|
|`http://cliente1.localhost:3000/sso`|**SSO Receiver**|**La Aduana:** Recibe el token por URL, lo guarda en el `localStorage` del subdominio y redirige al Dashboard.|

## 3. Acceso por Inquilino (Esquema Tenant - subdominio)

Rutas privadas protegidas por el `access_token`. Solo son accesibles si el usuario pasó por la "Aduana" o ya tiene una sesión activa en ese subdominio.

|   |   |   |
|---|---|---|
|**URL Ejemplo**|**Componente**|**Descripción**|
|`http://cliente1.localhost:3000/dashboard`|**Dashboard**|Panel principal con inventario y estadísticas filtradas por esquema.|
|`http://cliente1.localhost:3000/login`|**Login Local**|(Opcional) Acceso directo si el usuario ya conoce su subdominio.|

## 4. Endpoints de la API (Backend - Puerto 8000)

El Backend responde de forma dinámica según el **Host** de la petición. El puerto 8000 es el que procesa toda la lógica de datos.

|   |   |   |
|---|---|---|
|**Endpoint**|**Método**|**Función**|
|`/api/token/`|`POST`|Autentica al usuario y devuelve el JWT + el nombre del subdominio.|
|`/api/productos/`|`GET`|Lista los productos del tenant activo (identificado por el subdominio).|
|`/api/productos/`|`POST`|Crea un nuevo producto en el esquema correspondiente.|

### 💡 Notas para el Desarrollador

1. **Aislamiento de Cookies/Storage:** Recuerda que `localhost` no comparte datos con `cliente1.localhost`. Por eso la ruta `/sso` es vital.
    
2. **Redirección de Red:** Para que `cliente1.localhost` resuelva correctamente en tu máquina local, asegúrate de que el backend tenga el dominio registrado exactamente igual en la tabla `Domain`.
    
3. **CORS:** El backend permite peticiones desde cualquier subdominio de `.localhost` gracias a la configuración de `django-cors-headers`.

## 5. Documentación Interactiva de APIs

Para revisar todos los endpoints disponibles con sus parámetros, métodos y ejemplos:

|   |   |
|---|---|
|**URL**|**Propósito**|
|`http://localhost:8001/api/schema/swagger-ui/`|**Swagger UI** - Interfaz interactiva para probar endpoints. Usa el botón "Authorize" para autenticarse con JWT.|
|`http://localhost:8001/api/schema/redoc/`|**ReDoc** - Documentación limpia y profesional de todos los endpoints.|
|`http://localhost:8001/api/schema/`|**OpenAPI Schema** - Formato JSON estándar (importable en Postman, Insomnia, etc.)|

**Autenticación en Swagger:** Obtén un token en `/api/token/` con tus credenciales, luego en Swagger haz clic en "Authorize" y escribe: `Bearer <tu_access_token>`