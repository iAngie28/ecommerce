# Flujo de datos: JWT, Schemas y Dominios

## Mapa de relaciones en la base de datos

```
PostgreSQL
│
├── schema: public  ←──────────────── django-tenants lo gestiona
│   ├── customers_client          (tenants: Empresa 1, Empresa 2, ...)
│   ├── customers_domain          (dominios: empresa1.localhost, ...)
│   ├── customers_usuario         (TODOS los usuarios de todas las empresas)
│   └── django_tenants_blacklist  (tokens JWT invalidados)
│
├── schema: empresa_1  ←─────────────── datos de Empresa 1
│   └── app_negocio_producto      (productos solo de Empresa 1)
│
├── schema: empresa_2
│   └── app_negocio_producto      (productos solo de Empresa 2)
│
└── schema: empresa_3
    └── app_negocio_producto      (productos solo de Empresa 3)
```

## Flujo del JWT (token de autenticación)

### Contenido del JWT
```json
{
  "user_id": 5,
  "email": "user1@empresa1.local",
  "schema": "empresa_1",          ← añadido por MyTokenObtainPairSerializer
  "tenant_name": "Empresa 1",
  "exp": 1234567890,
  "token_type": "access"
}
```

### Cómo se genera
En `customers/serializers/usuario_serializers.py`:
```python
refresh = RefreshToken.for_user(user)
if user.tenant:
    refresh['schema'] = user.tenant.schema_name   # empresa_1
    refresh['tenant_name'] = user.tenant.name     # Empresa 1
```

### Cómo el backend responde al login
En `customers/services/auth_service.py`:
```python
return {
    'access': str(refresh.access_token),
    'refresh': str(refresh),
    'schema_name': user.tenant.schema_name,      # empresa_1
    'subdomain': domain_obj.domain,              # empresa1.localhost
    'user_name': user.email,
    'tenant_id': user.tenant.id,
}
```

## Cómo django-tenants identifica el tenant en cada request

```
Request HTTP
    │
    ▼
TenantMainMiddleware
    │
    ├── 1. Extrae hostname: request.get_host().split(':')[0]
    │      empresa1.localhost:8001 → empresa1.localhost
    │
    ├── 2. Busca en public.customers_domain
    │      WHERE domain = 'empresa1.localhost'
    │      → encuentra tenant_id → Empresa 1
    │
    ├── 3. Cambia el schema de PostgreSQL
    │      connection.set_tenant(tenant)
    │      → SET search_path = empresa_1, public
    │
    └── 4. Request continúa → ProductoViewSet.get_queryset()
               connection.schema_name == 'empresa_1'
               → Producto.objects.all()  ← solo los de empresa_1
```

## Por qué ALLOWED_HOSTS importa tanto

Django valida el `Host` header de cada request ANTES de que el middleware pueda procesar nada:

```
Request: empresa1.localhost:8001/api/productos/
     │
     ▼
Django valida ALLOWED_HOSTS
     │
     ├── SI 'empresa1.localhost' está en ALLOWED_HOSTS → continúa ✅
     └── SI NO está → lanza DisallowedHost
                          │
                          ▼
                    TenantMainMiddleware captura
                    → return HttpResponseNotFound()
                    → 404 con 0 bytes (NO llega al URL resolver)
```

Por eso `*localhost` (asterisco) no funciona — Django solo reconoce `.localhost` (punto).

## El localStorage es aislado por subdominio

El browser implementa aislamiento automático:

```
empresa1.localhost:3000    empresa2.localhost:3000    localhost:3000
       │                          │                        │
  localStorage                localStorage            localStorage
  access_token ←──────────┐      access_token ←──┐   (tokens del admin)
  refresh_token            │      refresh_token   │
  (de empresa1)            │      (de empresa2)   │
                           │                      │
              No puede acceder al de empresa2 ────┘
              No puede acceder al de localhost
```

Esto es lo que da el aislamiento real entre tenants en el frontend.

## Cómo agregar un nuevo tenant (checklist)

```bash
# 1. Crear el tenant en Django (se crea el schema en PostgreSQL automáticamente)
python manage.py shell
>>> from customers.models import Client, Domain
>>> t = Client.objects.create(schema_name='empresa_4', name='Empresa 4')
>>> Domain.objects.create(domain='empresa4.localhost', tenant=t, is_primary=True)
>>> exit()

# 2. Crear usuario para ese tenant
>>> from customers.models import Usuario
>>> u = Usuario.objects.create_user(
...     email='admin@empresa4.local',
...     password='password123',
...     tenant=t,
...     is_active=True
... )

# 3. En desarrollo: añadir al hosts file
#    127.0.0.1   empresa4.localhost

# 4. En producción: configurar DNS wildcard (ya cubre empresa4 automáticamente)
```
