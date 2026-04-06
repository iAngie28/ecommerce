# Arquitectura Multi-Tenant con Subdominios

## ¿Qué es Multi-Tenant?

Este sistema usa `django-tenants` para aislar completamente los datos de cada empresa (cliente) en esquemas separados de PostgreSQL. Cada empresa tiene:
- Su propio subdominio (`empresa1.tudominio.com`)
- Su propio esquema de BD (`empresa_1`)
- Sus propios productos, datos de negocio completamente aislados

Los datos de autenticación (usuarios) son **compartidos** en el esquema público.

---

## Flujo completo de autenticación y routing

```
                  DESARROLLO                         PRODUCCIÓN
─────────────────────────────────────────────────────────────────

1. Usuario abre:  localhost:3000/login          tudominio.com/login

2. Escribe:       user1@empresa1.local          user1@empresa1.com
                  password: user123456          password: *****

3. POST a:        localhost:8001/api/token/     tudominio.com/api/token/

4. Backend        autenticar → buscar tenant    autenticar → buscar tenant
   responde:      subdomain: empresa1.localhost subdomain: empresa1.tudominio.com
                  access: <JWT>                 access: <JWT>
                  refresh: <JWT>                refresh: <JWT>

5. Redirect:      empresa1.localhost:3000/sso   empresa1.tudominio.com/sso
                  ?token=<JWT>&refresh=<JWT>

6. SSO guarda     localStorage[empresa1.localhost]        
   tokens en:     access_token = <JWT>
                  refresh_token = <JWT>

7. Dashboard en:  empresa1.localhost:3000/dashboard       empresa1.tudominio.com/dashboard

8. API llama a:   empresa1.localhost:8001/api/productos/  empresa1.tudominio.com/api/productos/
                  ↓                                       ↓
                  Django detecta subdominio               Django detecta subdominio
                  → schema: empresa_1                     → schema: empresa_1
                  → devuelve productos de empresa1        → devuelve productos de empresa1
```

---

## Puertos y servicios

| Servicio | Desarrollo | Producción |
|----------|-----------|------------|
| Frontend (React) | `localhost:3000` | Puerto 80/443 (NGINX) |
| Backend (Django) | `localhost:8001` | Puerto 80/443 (NGINX proxy) |
| Base de datos | `localhost:5432` | `localhost:5432` (solo acceso local) |
| Login global | `localhost:3000/login` | `tudominio.com/login` |
| Dashboard empresa1 | `empresa1.localhost:3000` | `empresa1.tudominio.com` |

---

## Archivos clave del sistema

| Archivo | Rol |
|---------|-----|
| `backend/config/settings.py` | `TENANT_MODEL`, `ROOT_URLCONF`, `PUBLIC_SCHEMA_URLCONF` |
| `backend/config/settings_local.py` | `ALLOWED_HOSTS` (con `.localhost`), `CORS_ALLOWED_ORIGIN_REGEXES` |
| `backend/config/urls.py` | URL conf única para público y tenants |
| `backend/customers/serializers/usuario_serializers.py` | Auth: acepta `username` o `email` |
| `backend/customers/services/auth_service.py` | Retorna `subdomain` y `schema_name` en el JWT |
| `backend/app_negocio/views/producto_views.py` | Maneja schema público ([])) vs tenant (datos reales) |
| `frontend/src/services/api.js` | URL base dinámica según `window.location.hostname` |
| `frontend/src/components/Login.js` | Redirige a subdominio tras login |
| `frontend/src/App.js` | `SSOReceiver` guarda tokens del subdominio |

---

Ver también:
- [🛠 Configuración por entorno](./entornos.md) — desarrollo local vs producción VPS
- [🗺 Flujo de datos](./flujo_datos.md) — JWT, schemas, dominios
