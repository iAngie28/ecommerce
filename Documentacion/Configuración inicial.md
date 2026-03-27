Sigue estos pasos para poner en marcha el proyecto localmente después de clonar el repositorio.

## 1. Requisitos Previos

- PostgreSQL instalado y corriendo.
    
- Crear una base de datos vacía llamada `ecommerce_db` (o el nombre configurado en `settings.py`).
    

## 2. Configuración del Backend

**Directorio:** `\backend\`

1. **Crear y activar entorno virtual:**
    
    ```
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    ```
    
2. **Instalar dependencias:**
    
    ```
    pip install -r requirements.txt
    ```
    
3. **Ejecutar migraciones de esquemas:**
    
    ```
    python manage.py migrate_schemas
    ```
    

## 3. Registro de Tenant (Inquilino)

Como no existe interfaz de creación de clientes, debe hacerse por consola para poder entrar al sistema.

1. **Abrir shell de Django:**
    
    ```
    python manage.py shell
    ```
    
2. **Ejecutar registro (Copiar y pegar):**
    
    ```
    from app_usuarios.models import Client, Domain
    tenant = Client.objects.create(schema_name='cliente1', name='Cliente 1')
    Domain.objects.create(domain='cliente1.localhost', tenant=tenant, is_primary=True)
    exit()
    ```
    

## 4. Crear Usuario Administrador

El usuario debe crearse específicamente dentro del esquema del cliente creado.

```
python manage.py tenant_command createsuperuser --schema=cliente1
```

## 5. Configuración del Frontend

**Directorio:** `\frontend\`

1. **Instalar módulos de Node:**
    
    ```
    npm install
    ```
    
2. **Iniciar servidor de desarrollo:**
    
    ```
    npm start
    ```
    

## 6. Prueba de Acceso

1. Iniciar el backend: `python manage.py runserver`
    
2. Abrir en el navegador: `http://cliente1.localhost:3000/login`
    
3. Ingresar las credenciales creadas en el paso 4.