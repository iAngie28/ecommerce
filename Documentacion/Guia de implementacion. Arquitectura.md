## 1. Entorno de Backend

**Directorio inicial:** `C:\Users\nextr\Desktop\SI@\Trabajo Grupal\`

1. **Creación del entorno virtual:**
    
    - Comando: `python -m venv venv`
        
    - Uso: Aislar las dependencias del proyecto de la instalación global de Python.
        
2. **Instalación de dependencias base:**
    
    - Comando: `pip install -r requirements.txt`
        
    - **django-tenants:** Gestión de aislamiento de datos mediante esquemas de PostgreSQL.
        
    - **djangorestframework:** Construcción de la interfaz de programación de aplicaciones (API).
        
    - **psycopg2-binary:** Adaptador para la comunicación con el motor de base de datos PostgreSQL.
        
    - **djangorestframework-simplejwt:** Gestión de tokens JWT para autenticación.
        

## 2. Configuración Multi-tenant y Arquitectura de Capas

**Directorio:** `\backend\`

### 2.1 Infraestructura Base (core/)

El sistema centraliza la lógica reutilizable en la carpeta `core/`:

- **`core/services.py`**: Clase `BaseService` que proporciona CRUD genérico a todos los servicios.
- **`core/mixins.py`**: Mixins que inyectan funcionalidad común:
    - `MultiTenantMixin`: Filtra automáticamente los datos por esquema (schema-based multi-tenancy).
    - `AuditoriaMixin`: Registra automáticamente todas las acciones (CREAR, EDITAR, ELIMINAR) en la Bitácora.
- **`core/views.py`**: `BaseViewSet` que hereda de ambos Mixins y `ModelViewSet`.
- **`core/validators.py`**: Validadores centralizados por dominio (validaciones de negocio, no solo serializers).
- **`core/exceptions.py`**: Excepciones personalizadas del negocio.

### 2.2 Aplicaciones Modulares

Cada aplicación (customers, app_negocio) sigue la estructura:

```
app/
├── models/           → Definición de tablas (sin lógica de negocio)
├── serializers/      → Conversión a JSON + validaciones básicas
├── services/         → Lógica de negocio (heredan de BaseService)
├── views/            → Orquestadores HTTP (heredan de BaseViewSet)
├── admin/            → Interfaz administrativa
└── tests/            → Tests unitarios e integración
```

## 3. Ejecución de Migraciones

**Directorio:** `\backend\`

- Comando: `python manage.py migrate_schemas`
    
- Uso: Crear las tablas globales en el esquema `public` y las tablas de negocio en los esquemas de cada cliente.
    

## 4. Seguridad y API

**Directorio:** `\backend\`

- CORS configurado para permitir peticiones desde el frontend (puerto 3000).
- JWT para autenticación sin estado.
- Multi-tenant aislamiento garantizado por `django-tenants` (schema-based).

## 5. Modelo de Negocio (Aplicaciones)

### Estructura Típica de un CRUD (Ej: Producto)

**1. Modelo** (`models/producto.py`):
```python
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
```

**2. Serializer** (`serializers/producto_serializer.py`):
```python
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock']  # ✅ Lista explícita (no __all__)
```

**3. Service** (`services/producto_service.py`):
```python
class ProductoService(BaseService):
    def __init__(self):
        super().__init__(Producto)
    
    def rebajar_stock(self, producto, cantidad):
        if producto.stock < cantidad:
            raise ValueError("Stock insuficiente")
        producto.stock -= cantidad
        producto.save()
        return producto
```

**4. View** (`views/producto_views.py`):
```python
from core.views import BaseViewSet

class ProductoViewSet(BaseViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    modulo_auditoria = "Producto"  # ✅ AuditoriaMixin usa esto
```

**Beneficio:** La auditoría se registra automáticamente (sin código manual). MultiTenantMixin filtra automáticamente por esquema.

## 6. Entorno de Frontend

**Directorio:** `\frontend\`

1. **Instalación de librerías:**
    
    - Comando: `npm install`
        
    - **axios:** Cliente HTTP configurado con interceptores para inyectar el token JWT en las cabeceras.
        
    - **react-router-dom:** Gestión de rutas y navegación.
        
    - **lucide-react:** Librería de iconos para la interfaz.
        
    - **tailwind css:** Framework de estilos.
        

## 7. Ejecución de servicios

1. **Backend:** `python manage.py runserver`
    
2. **Frontend:** `npm start`