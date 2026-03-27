## 1. Entorno de Backend

**Directorio inicial:** `C:\Users\nextr\Desktop\SI@\Trabajo Grupal\`

1. **Creación del entorno virtual:**
    
    - Comando: `python -m venv venv`
        
    - Uso: Aislar las dependencias del proyecto de la instalación global de Python.
        
2. **Instalación de dependencias base:**
    
    - Comando: `pip install django django-tenants djangorestframework psycopg2-binary`
        
    - **django-tenants:** Gestión de aislamiento de datos mediante esquemas de PostgreSQL.
        
    - **djangorestframework:** Construcción de la interfaz de programación de aplicaciones (API).
        
    - **psycopg2-binary:** Adaptador para la comunicación con el motor de base de datos PostgreSQL.
        

## 2. Configuración Multi-tenant

**Directorio:** `\backend\`

1. **Definición de aplicaciones (settings.py):**
    
    - División de aplicaciones en `SHARED_APPS` (dominio, clientes) y `TENANT_APPS` (app_negocio para productos).
        
    - Uso de `django_tenants.routers.TenantSyncRouter` para direccionar las consultas al esquema correspondiente.
        
2. **Ejecución de migraciones:**
    
    - Comando: `python manage.py migrate_schemas`
        
    - Uso: Crear las tablas globales en el esquema `public` y las tablas de negocio en los esquemas de cada cliente.
        

## 3. Seguridad y API

**Directorio:** `\backend\`

1. **Instalación de seguridad y tokens:**
    
    - Comando: `pip install django-cors-headers djangorestframework-simplejwt`
        
    - **django-cors-headers:** Middleware para permitir peticiones desde el origen del frontend (puerto 3000).
        
    - **simplejwt:** Implementación de JSON Web Tokens para autenticación sin estado.
        
2. **Configuración de acceso:**
    
    - Configuración de `CORS_ALLOW_ALL_ORIGINS = True` en `settings.py` para habilitar el tráfico entre puertos durante el desarrollo.
        

## 4. Modelo de Negocio (Productos)

**Directorio:** `\backend\app_negocio\`

1. **Creación de modelos:**
    
    - Archivo: `models.py`. Definición de la clase `Producto` (nombre, descripción, precio, stock).
        
2. **Exposición de datos:**
    
    - Archivo: `serializers.py` (uso de `ModelSerializer`).
        
    - Archivo: `views.py` (uso de `ModelViewSet`).
        
    - Uso: Operaciones CRUD filtradas automáticamente por el esquema del inquilino activo.
        

## 5. Entorno de Frontend

**Directorio:** `\frontend\`

1. **Inicialización del proyecto:**
    
    - Comando: `npx create-react-app .`
        
2. **Instalación de librerías de interfaz:**
    
    - Comando: `npm install axios react-router-dom lucide-react`
        
    - **axios:** Cliente HTTP configurado con interceptores para inyectar el token JWT en las cabeceras.
        
    - **react-router-dom:** Gestión de rutas y navegación.
        
    - **lucide-react:** Librería de iconos para la interfaz.
        

## 6. Gestión de Inquilinos por Consola

Debido a la ausencia de una interfaz administrativa (CRUD) para la gestión de inquilinos en esta fase, todas las operaciones de registro deben ejecutarse vía consola.

**Directorio:** `\backend\`

1. **Registro de Tenant y Dominio:**
    
    - Comando: `python manage.py shell`
        
    - Ejecución interna:
        
        ```
        from app_usuarios.models import Client, Domain
        # Crear el inquilino
        tenant = Client.objects.create(schema_name='cliente1', name='Cliente 1')
        # Vincular el dominio para identificación por URL
        Domain.objects.create(domain='cliente1.localhost', tenant=tenant, is_primary=True)
        ```
        
2. **Identificación por URL:**
    
    - El sistema identifica al inquilino mediante el `Middleware` de `django-tenants`.
        
    - Proceso: La petición entrante (ej: `cliente1.localhost:8000`) es interceptada; el host es comparado con la tabla `Domain`. Al hallar coincidencia, se establece el `search_path` de PostgreSQL al esquema `cliente1`.
        
3. **Creación de usuarios por esquema:**
    
    - Comando: `python manage.py tenant_command createsuperuser --schema=cliente1`
        
    - Uso: Registrar credenciales administrativas aisladas dentro del esquema del cliente.
        
4. **Poblamiento de productos por esquema:**
    
    - Comando: `python manage.py tenant_command shell --schema=cliente1`
        
    - Ejecución interna:
        
        ```
        from app_negocio.models import Producto
        Producto.objects.create(nombre="Laptop", precio=1200, stock=5)
        ```
        

## 7. Ejecución de servicios

1. **Backend:** `python manage.py runserver`
    
2. **Frontend:** `npm start`