
## 1. Acceso General (Esquema Público)

Estas rutas se utilizan para la gestión global de la plataforma, como la creación de nuevos clientes o la administración del sistema compartido.

|   |   |   |
|---|---|---|
|**URL**|**Componente**|**Descripción**|
|`http://localhost:3000/login`|Login|Acceso para administradores globales del SaaS.|
|`http://localhost:8000/admin/`|Django Admin|Panel nativo para gestionar la tabla de clientes y dominios.|

## 2. Acceso por Inquilino (Esquema Tenant)

Estas rutas son específicas para cada cliente. El sistema identifica automáticamente a qué base de datos conectarse mediante el subdominio en la URL.

|   |   |   |
|---|---|---|
|**URL Ejemplo**|**Componente**|**Descripción**|
|`http://cliente1.localhost:3000/login`|Login Tenant|Inicio de sesión exclusivo para los empleados/dueños de "Cliente 1".|
|`http://cliente1.localhost:3000/dashboard`|Dashboard|Panel de control con el inventario y métricas privadas del tenant.|

## 3. Endpoints de la API (Backend - Puerto 8000)

La API procesa los datos según el `HOST` de la petición. Si la petición viene de `cliente1.localhost`, devolverá solo datos de ese esquema.

|   |   |   |
|---|---|---|
|**Endpoint**|**Método**|**Función**|
|`/api/token/`|POST|Genera el token de acceso. Busca al usuario en el esquema indicado por la URL.|
|`/api/productos/`|GET|Lista los productos pertenecientes al tenant actual.|
|`/api/productos/`|POST|Registra un nuevo producto en la base de datos del tenant activo.|

### 💡 Nota Importante para Pruebas

Para que las rutas de los tenants funcionen, es obligatorio que el subdominio (ej: `cliente1`) esté previamente registrado en la tabla de **Dominios** del backend y, preferiblemente, mapeado en el archivo `hosts` del sistema operativo.