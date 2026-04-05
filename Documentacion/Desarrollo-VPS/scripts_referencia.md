# Scripts Utiles — Referencia

Todos los scripts viven en `/scripts_utiles/` y son ejecutados por `launcher.py`.
También se pueden correr directamente desde `/backend`:
```bash
cd backend
..\venv\Scripts\python.exe ..\scripts_utiles\<script>.py
```

---

## db_reset.py — Resetear Base de Datos

**¿Qué hace?**
Destruye y recrea la base de datos completa. Útil cuando las migraciones están en un estado inconsistente o quieres empezar de cero.

**Proceso:**
1. Elimina TODOS los schemas de PostgreSQL (empresa_1, empresa_2, public...)
2. Elimina y recrea la BD
3. Ejecuta `makemigrations` + `migrate` (crea la estructura limpia)
4. Opcionalmente crea un superusuario

**Cuándo usarlo:**
- Al cambiar modelos que afectan la estructura de schemas
- Cuando `migrate` falla por conflictos de migraciones
- Para tener una BD limpia antes de una demo

> ⚠️ **DESTRUCTIVO**: borra todos los datos. No usar en producción.

---

## db_seed.py — Popular con Datos de Prueba

**¿Qué hace?**
Crea datos de prueba realistas en la BD. Tiene 3 modos:

| Modo | Tenants | Usuarios/tenant | Productos/tenant |
|------|---------|----------------|-----------------|
| Demo | 1 | 5 | 10 |
| Development | 3 | 5 | 10 |
| Production-like | 4 (nombres realistas) | 5 | 15 |

**Datos del modo Development:**

| Tenant | Schema | Dominio local |
|--------|--------|--------------|
| Empresa 1 | `empresa_1` | `empresa1.localhost` |
| Empresa 2 | `empresa_2` | `empresa2.localhost` |
| Empresa 3 | `empresa_3` | `empresa3.localhost` |

**Credenciales generadas:**
- Email: `user{1-5}@empresa{1-3}.local`
- Password: `user123456`
- Todos activos: `is_active=True`
- Tenant FK correctamente asignado: `tenant=<Client>`

> ⚠️ Los usuarios deben crearse con `tenant=tenant` explícito (FK obligatorio para el routing de subdominios)

---

## manage_users.py — Gestión de Usuarios

**¿Qué hace?**
CLI interactivo para gestionar usuarios en la BD sin tocar el admin de Django.

**Operaciones:**
- `create` — Crear usuario (pide email, password, tenant)
- `list` — Listar todos los usuarios con su tenant asignado
- `delete` — Eliminar usuario por email

**Útil para:**
- Crear usuarios de prueba rápidamente
- Verificar asignaciones de tenant (`user.tenant.schema_name`)
- Desactivar/activar usuarios

---

## test_shell.py — Consola de Pruebas

**¿Qué hace?**
Shell interactivo con Django configurado para hacer pruebas directas sobre la BD.

Equivale a `manage.py shell` pero con imports pre-configurados:
```python
# Imports disponibles automáticamente:
from customers.models import Usuario, Client
from app_negocio.models import Producto
from django_tenants.utils import tenant_context, schema_context
from django.db import connection
```

**Ejemplos de uso:**
```python
# Ver schema activo
connection.schema_name

# Cambiar a contexto de empresa_1
with schema_context('empresa_1'):
    print(Producto.objects.count())

# Ver usuario y su tenant
u = Usuario.objects.get(email='user1@empresa1.local')
print(u.tenant.schema_name)  # empresa_1
```

---

## db_config.py — Configuración de Base de Datos

**¿Qué hace?**
Asistente para configurar las variables de conexión en el `.env` sin editarlo manualmente.

**Modos:**
- `basic` — Preset para desarrollo local (localhost, puerto 5432)
- `advanced` — Configuración manual campo a campo
- `presets` — Ver configuraciones predefinidas
- `test` — Probar que la conexión es exitosa
- `field` — Cambiar un campo específico del .env

---

## nginx_config.py — Configuración NGINX para VPS

**¿Qué hace?**
Genera y gestiona los servicios systemd para Django (Gunicorn) y el servidor de React en producción.

**Solo relevante en VPS (Linux con systemd)**

**Operaciones:**
- `django-service` — Crea el servicio systemd para Django/Gunicorn
- `frontend-service` — Crea el servicio para el frontend
- `status` — Ver estado de los servicios
- `logs` — Ver logs en tiempo real
- `reload-nginx` — Recarga la config de NGINX
- `restart` — Reinicia un servicio
- `delete-service` — Elimina un servicio

---

## migrations.py — Gestión de Migraciones

**¿Qué hace?**
Wrapper sobre `manage.py makemigrations` y `manage.py migrate` con soporte para `django-tenants`.

**Con `django-tenants`, las migraciones son de dos tipos:**
- `migrate_schemas --shared` → aplica a las apps de SHARED_APPS (public schema)
- `migrate_schemas` → aplica a TODOS los tenant schemas (empresa_1, empresa_2, etc.)

---

## system_manager.py — Gestión del Sistema

**¿Qué hace?**
Herramientas de mantenimiento del servidor.

**Operaciones:**
- `update-django` — `pip install -r requirements.txt --upgrade`
- `update-npm` — `npm update`
- `update-system` — `apt update && apt upgrade` (Linux)
- `generate-secrets` — Genera `DJANGO_SECRET_KEY`, `JWT_SECRET`, etc. y los guarda en `.env`
- `health-check` — Verifica que todos los servicios están corriendo
