# Documentación Técnica: Backend (Django & Python)

Este archivo detalla las dependencias y herramientas utilizadas en el servidor para gestionar la lógica multi-tenant y la API.

|   |   |   |
|---|---|---|
|**Librería**|**Propósito**|**Resumen de Uso**|
|**Django**|Framework Web|El "motor" principal que gestiona la lógica de negocio y la base de datos.|
|**django-tenants**|Multi-tenancy|Permite que cada cliente tenga su propio esquema en PostgreSQL, garantizando el aislamiento de datos.|
|**Django REST Framework**|API REST|Transforma los modelos de Django en JSON para la comunicación con el frontend.|
|**drf-spectacular**|Documentación API|Genera automáticamente documentación Swagger/OpenAPI interactiva con soporte JWT.|
|**django-cors-headers**|Seguridad (CORS)|Permite que el servidor acepte peticiones desde el puerto de React (:3000).|
|**djangorestframework-simplejwt**|Autenticación JWT|Gestiona el inicio de sesión seguro mediante tokens.|
|**Psycopg2-binary**|Driver de BD|Conector oficial para la base de datos PostgreSQL.|

### ⚙️ Notas de Configuración

- **Mapeo de Dominios**: Uso de la tabla `Domain` para vincular subdominios con esquemas.
    
- **Aislamiento de Usuarios**: Creación de administradores por esquema con `tenant_command createsuperuser`.
# Documentación Técnica: Frontend (React & JavaScript)

Este archivo detalla las bibliotecas utilizadas para construir la interfaz de usuario moderna y adaptativa de la tienda.

|   |   |   |
|---|---|---|
|**Librería**|**Propósito**|**Resumen de Uso**|
|**React**|Biblioteca de UI|Gestiona los componentes visuales y el estado de la aplicación.|
|**React Router DOM**|Enrutamiento|Permite la navegación entre Login y Dashboard sin recargar la página.|
|**Axios**|Cliente HTTP|Realiza las peticiones a la API e incluye interceptores para el token JWT.|
|**Lucide React**|Iconografía|Proporciona los iconos vectoriales profesionales del Dashboard.|
|**Tailwind CSS**|Estilizado (CSS)|Framework de utilidades para el diseño rápido y responsivo.|

### 🛠️ Herramientas de Entorno

- **Vite/Create React App**: Entorno de ejecución y compilación.
    
- **Local Storage**: Uso para persistir el `access_token` del usuario.

---

## 📖 Acceso a Documentación de APIs (drf-spectacular)

Con **drf-spectacular** integrado, la documentación interactiva se genera automáticamente:

### Endpoints de Documentación

Con el backend corriendo en `http://localhost:8001`:

1. **Swagger UI (Recomendado para pruebas):**
   ```
   http://localhost:8001/api/schema/swagger-ui/
   ```
   - Interfaz interactiva y amigable
   - Botón "Authorize" para autenticación JWT
   - Prueba endpoints directamente desde el navegador

2. **ReDoc (Mejor para lectura):**
   ```
   http://localhost:8001/api/schema/redoc/
   ```
   - Documentación limpia y profesional
   - Excelente para compartir con el equipo

3. **OpenAPI JSON (Para importar):**
   ```
   http://localhost:8001/api/schema/
   ```
   - Formato estándar OpenAPI 3.0
   - Importable en Postman, Insomnia, etc.