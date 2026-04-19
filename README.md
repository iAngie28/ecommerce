# PROYECTO E-COMMERCE MULTI-TENANT

Sistema completo de e-commerce SaaS con Django + React + PostgreSQL

## 🚀 Inicio Rápido

### Windows
```bash
# 1. Setup inicial
dev.bat

# 2. Lanzador de herramientas
launcher.bat
```

### Linux / Mac
```bash
# 1. Setup inicial
./dev.sh

# 2. Lanzador de herramientas
./launcher.sh
```

---

## 📁 Estructura del Proyecto

```
.
├── backend/                    # Django + django-tenants
│   ├── config/                # Configuración de Django
│   ├── app_negocio/          # App de productos
│   ├── customers/            # App de usuarios y tenants
│   ├── scripts_utiles/       # Scripts reutilizables
│   └── manage.py             # Comando principal de Django
│
├── frontend/                   # React 18+
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   ├── services/         # API client (axios)
│   │   └── contexts/         # Context de tenant
│   └── package.json
│
├── nginx/                      # Configuración Nginx (VPS)
│   └── prod.vps.conf         # Proxy HTTP
│
├── Documentacion/             # Documentación completa
│   ├── ARQUITECTURA.md       # Arquitectura del sistema
│   ├── Configuración inicial.md
│   ├── Login.md
│   ├── Rutas.md
│   └── ANEXOS/
│
├── .env                       # Configuración (ÚNICO archivo)
├── .env.example              # Template de configuración
├── dev.bat                   # Setup desarrollo (Windows)
├── dev.sh                    # Setup desarrollo (Linux)
├── prod.sh                   # Setup producción (VPS)
├── launcher.bat              # Herramientas (Windows)
├── launcher.sh               # Herramientas (Linux)
└── LANZADORES.md            # Guía de herramientas
```

---

## 🛠️ Herramientas Disponibles

### Lanzador Interactivo
Menu visual para:
- ✓ Configuración (dev/prod)
- ✓ Tests, migraciones, linting
- ✓ Gestión de servicios VPS
- ✓ Crear usuarios, dominios, SSL

**Uso:**
```bash
# Windows
launcher.bat

# Linux
./launcher.sh
```

👉 **Ver [LANZADORES.md](LANZADORES.md) para más detalles**

---

## ⚙️ Configuración

Todo se controla desde un **único `.env`** en la raíz:

```ini
# Entorno
ENVIRONMENT=development          # development o production
DEBUG=True

# Dominios (hostname se auto-detecta)
DOMAIN_MAIN=localhost
DOMAIN_ALLOWED_HOSTS=

# Puertos
DJANGO_PORT=8001
REACT_PORT=3000
NGINX_PORT=80

# API Frontend
REACT_APP_API_URL=http://localhost:8001/api

# Database
DATABASE_NAME=mi_saas_db
DATABASE_USER=postgres
DATABASE_PASSWORD=adm123
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432

# ... más variables
```

👉 **Ver [.env.example](.env.example) para configuración completa**

---

## 🚀 Modo Desarrollo

### 1. Setup Inicial
```bash
# Windows
dev.bat

# Linux
./dev.sh
```

Esto:
- ✓ Copia `.env` a backend y frontend
- ✓ Crea `venv` de Python
- ✓ Instala dependencias (pip, npm)
- ✓ Ejecuta migraciones

### 2. Iniciar Servicios

**Terminal 1 - Django:**
```bash
cd backend
venv\Scripts\activate        # Windows: venv\Scripts\activate.bat
python manage.py runserver 127.0.0.1:8001
```

**Terminal 2 - React:**
```bash
cd frontend
npm start
```

**Acceso:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8001
- Admin: http://localhost:8001/admin
- API: http://localhost:8001/api

---

## 🌐 Modo Producción (VPS)

### 1. Preparar Variables
```bash
# Abrir lanzador
./launcher.sh

# Configuración > Configurar PRODUCCIÓN
# Ingresar dominio y hosts
```

### 2. Ejecutar Setup VPS
```bash
sudo ./prod.sh
```

Instala y configura:
- ✓ PostgreSQL
- ✓ Python + Django
- ✓ Node.js + React
- ✓ Nginx (proxy HTTP)
- ✓ Supervisor (servicio de Django)
- ✓ Systemd
- ✓ SSL con Let's Encrypt

### 3. Crear Dominio
```bash
sudo ./launcher.sh

# Servicios VPS > Crear dominio
```

### 4. Instalar SSL
```bash
sudo ./launcher.sh

# Servicios VPS > Instalar SSL (Let's Encrypt)
```

---

## 📊 Scripts Utiles

### Desde Lanzador
```
launcher.bat / launcher.sh
  → Menú 2: Scripts Utiles
    ├─ Tests
    ├─ Lint (flake8)
    ├─ Migraciones (Ver/Crear/Aplicar)
    ├─ Seed Database
    └─ Reset Database

  → Menú 3: Gestión de Datos
    ├─ Reset: Completo / Solo datos / Tenants / Usuarios
    ├─ Seeders: Demo / Development / Production
    └─ Usuarios: Crear, editar, eliminar, listar, reset password

  → Menú 4: Consola de Pruebas Interactiva
    └─ Shell de Django con datos precargados
```

### Desde Terminal
```bash
# Reset de BD
python scripts_utiles/db_reset.py all            # Reset completo
python scripts_utiles/db_reset.py data           # Solo datos
python scripts_utiles/db_reset.py tenants        # Solo tenants

# Seeders
python scripts_utiles/db_seed.py demo            # 1 tenant
python scripts_utiles/db_seed.py dev             # 3 tenants
python scripts_utiles/db_seed.py prod            # Empresas

# Usuarios
python scripts_utiles/manage_users.py list       # Listar
python scripts_utiles/manage_users.py create     # Crear
python scripts_utiles/manage_users.py edit       # Editar
python scripts_utiles/manage_users.py delete     # Eliminar
python scripts_utiles/manage_users.py reset      # Reset password
python scripts_utiles/manage_users.py bulk-create # Batch

# Consola interactiva
python scripts_utiles/test_shell.py              # Shell con datos

# Tests
python scripts_utiles/test.py django             # Tests de Django
python scripts_utiles/test.py lint               # Linter
python scripts_utiles/migrations.py show         # Migraciones
```

---

## 🔐 Multi-Tenant (Clientes)

### Cómo Funciona
- ✓ Base de datos PostgreSQL con schemas por tenant
- ✓ Dominio único por cliente
- ✓ Usuarios aislados por tenant
- ✓ Datos independientes por tenant

### Crear Nuevo Tenant
```bash
cd backend
python manage.py shell

# En el shell:
from customers.models import Tenant, TenantUser
tenant = Tenant.objects.create(name="Mi Empresa", slug="mi-empresa")
TenantUser.objects.create(tenant=tenant, email="admin@miempresa.com", ...)
```

Luego asignar dominio:
```bash
# Desde lanzador
Servicios VPS > Crear dominio

# O manualmente agregar a DOMAIN_ALLOWED_HOSTS en .env
```

---

## 🔌 Arquitectura de Red

### Desarrollo (localhost)
```
React (3000) ──http──> Django (8001) ──db──> PostgreSQL (5432)
```

Sin Nginx, conexión directa.

### Producción (VPS)
```
Cliente
   │
   └──> Nginx (80/443)
         ├──> /api ──> Django (8001, privado)
         └──> / ──> React (3000, privado)
              │
              └──> PostgreSQL (5432, privado)
```

Nginx como proxy inverso, servicios en interno.

---

## 📝 Documentación Completa

- **[ARQUITECTURA.md](Documentacion/ARQUITECTURA.md)** - Arquitectura completa
- **[Plantilla Prompt IA Generador](Documentacion/Plantilla%20Prompt%20IA%20Generador.md)** - Esquema reusable para generar proyectos con IA
- **[LANZADORES.md](LANZADORES.md)** - Guía de herramientas
- **[Configuración inicial.md](Documentacion/Configuración%20inicial.md)** - Setup inicial
- **[Login.md](Documentacion/Login.md)** - Sistema de autenticación
- **[Rutas.md](Documentacion/Rutas.md)** - API endpoints

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
```bash
# Activar venv
cd backend
source venv/bin/activate        # Linux/Mac
# o
venv\Scripts\activate.bat       # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### "Cannot GET /api"
Asegúrate que Django está corriendo en puerto 8001:
```bash
python manage.py runserver 127.0.0.1:8001
```

### "Connection refused" en React
Verifica `.env`:
```ini
REACT_APP_API_URL=http://localhost:8001/api
```

### "Permission denied" en prod.sh
```bash
chmod +x prod.sh
sudo ./prod.sh
```

---

## 📞 Soporte

Ver documentación en `/Documentacion/` o ejecutar:
```bash
./launcher.sh
# Ayuda
```

---

## 📄 Licencia

Proyecto privado. Todos los derechos reservados.

---

**Última actualización:** Abril 2026
