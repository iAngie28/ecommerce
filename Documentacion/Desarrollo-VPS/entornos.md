# Configuración por entorno: Desarrollo vs Producción VPS

## 1. Desarrollo Local

### Requisitos únicos de desarrollo

#### a) Fichero `hosts` de Windows (una sola vez, admin)
Ubicación: `C:\Windows\System32\drivers\etc\hosts`

```
# MiQhatu - Subdominios de tenant locales
127.0.0.1   empresa1.localhost
127.0.0.1   empresa2.localhost
127.0.0.1   empresa3.localhost
```

> ⚠️ Sin esto, el browser no puede resolver `empresa1.localhost` y el redirect del login fallará.

#### b) ALLOWED_HOSTS — wildcard correcto
En `backend/config/settings_local.py`:
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    DEVICE_HOSTNAME,
    '.localhost',     # ← CORRECTO: cubre empresa1.localhost, empresa2.localhost, etc.
    #  ↑ NO usar '*localhost' — ese NO es un wildcard válido en Django
]
```

#### c) CORS — regex dinámica
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://\w+\.localhost:\d+$",  # Cubre CUALQUIER subdominio sin listar uno a uno
]
```

#### d) Frontend API base URL
En `frontend/src/services/api.js`:
```js
const hostname = window.location.hostname; // empresa1.localhost
const backendPort = process.env.REACT_APP_API_PORT || '8001';
const API_BASE_URL = `http://${hostname}:${backendPort}/api`;
// empresa1.localhost:3000 → llama a empresa1.localhost:8001/api
// localhost:3000          → llama a localhost:8001/api
```

### Cómo levantar desarrollo
```bash
python launcher.py     # desde la raíz del proyecto
# Inicia Django en 127.0.0.1:8001 y React en localhost:3000
```

### Credenciales de prueba (seeder de desarrollo)
| Email | Contraseña | Subdominio |
|-------|-----------|-----------|
| user1@empresa1.local | user123456 | empresa1.localhost:3000 |
| user1@empresa2.local | user123456 | empresa2.localhost:3000 |
| user1@empresa3.local | user123456 | empresa3.localhost:3000 |

---

## 2. Producción — VPS

### Arquitectura recomendada

```
Internet
    │
    ▼
[NGINX :443]  ← SSL termination
    │
    ├── tudominio.com         → React (build estático)
    ├── empresa1.tudominio.com → React (mismo build)
    │
    └── /api/*  (proxy pass)  → Django Gunicorn :8001
```

### a) DNS — Wildcard subdomain
En tu proveedor de DNS (Cloudflare, etc.):
```
A     tudominio.com         → <IP_VPS>
A     *.tudominio.com       → <IP_VPS>   ← ¡el wildcard es la clave!
```

### b) NGINX — configuración
```nginx
server {
    listen 443 ssl;
    server_name *.tudominio.com tudominio.com;

    # SSL (Let's Encrypt con wildcard)
    ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem;

    # API → Django
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;          # ← CRÍTICO: pasa el subdominio
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Frontend → React build
    location / {
        root /var/www/miqhatu/frontend/build;
        try_files $uri /index.html;
    }
}
```

> 🔴 `proxy_set_header Host $host;` es **crítico**. Sin esto, Django recibe `localhost` en vez del subdominio, el middleware no puede identificar el tenant y todo falla.

### c) ALLOWED_HOSTS en producción
En `settings_local.py` (environment = 'production'):
```python
ALLOWED_HOSTS = [
    'tudominio.com',
    '.tudominio.com',   # ← wildcard para todos los subdominios
]
```

### d) CORS en producción
```python
CORS_ALLOWED_ORIGINS = [
    "https://tudominio.com",
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.tudominio\.com$",  # cubre todos los subdominios
]
CORS_ALLOW_CREDENTIALS = True
```

### e) Crear dominios de tenant en la BD (producción)
Al crear un nuevo cliente en producción, se debe registrar su dominio:
```python
from customers.models import Client, Domain
tenant = Client.objects.get(schema_name='empresa_xyz')
Domain.objects.get_or_create(
    domain='empresaxyz.tudominio.com',
    defaults={'tenant': tenant, 'is_primary': True}
)
```

### f) Variables de entorno en VPS
En `.env` (producción):
```env
ENVIRONMENT=production
DJANGO_SECRET_KEY=<clave-secreta-larga-y-aleatoria>
DATABASE_URL=postgres://user:pass@localhost:5432/miqhatu_db
DOMAIN=tudominio.com
FRONTEND_URL=https://tudominio.com
```

---

## 3. Troubleshooting rápido

| Síntoma | Causa probable | Solución |
|---------|---------------|---------|
| `404` al llamar API desde subdominio | `ALLOWED_HOSTS` sin `.localhost` | Cambiar `*localhost` → `.localhost` |
| CORS error con credenciales | `CORS_ALLOW_CREDENTIALS = False` | Activarlo en `settings_local.py` |
| Redirige al subdominio pero da blank page | Hosts file no editado | Añadir entrada en `/etc/hosts` o `hosts` de Windows |
| Login OK pero productos vacíos `[]` | Token de antes del fix — genera uno nuevo | Logout + Login de nuevo |
| `DisallowedHost` en logs | ALLOWED_HOSTS no incluye el subdominio | Revisar `.localhost` o `.tudominio.com` |
| Tenant 404 en producción | `proxy_set_header Host $host` falta en NGINX | Añadir al bloque `location /api/` |
