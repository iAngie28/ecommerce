Sigue estos pasos para poner en marcha el proyecto eCommerce Multi-tenant SaaS.

---

## 🎯 Requisitos Previos

- **PostgreSQL** instalado y corriendo en `localhost:5432`
- **Python 3.9+** instalado
- **Node.js 16+** instalado
- Base de datos **`mi_saas_db`** (usuario: `postgres`, contraseña: `adm123`)

---

## 📋 Paso 1: Configurar el Backend (Django)

### 1.1 Activar entorno virtual en la terminal de vscode 

**En Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
venv\Scripts\activate
```

**En Mac/Linux:**
```bash
source venv/bin/activate
```

### 1.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 1.3 Ejecutar migraciones de esquemas

```bash
python manage.py migrate_schemas
```

### 1.4 Poblar la Base de Datos con datos de prueba

**En Terminal 1:**
```bash
python manage.py runserver 0.0.0.0:8000
```

**En Terminal 2 (con venv activado):**
```bash
python seed_db.py
```

Esto crea automáticamente:
- ✅ Tenant **cliente1** → "Tienda de Tecnología"
- ✅ Tenant **cliente2** → "Boutique de Ropa"  
- ✅ Usuario **adm1** / contraseña **123** (cliente1)
- ✅ Usuario **adm2** / contraseña **123** (cliente2)
- ✅ Dominios: `cliente1.localhost`, `cliente2.localhost`, `192.168.56.1`
- ✅ Productos de prueba en cada tenant

---

## 🎨 Paso 2: Configurar el Frontend (React)

### 2.1 Instalar dependencias

```bash
cd frontend
npm install
```

### 2.2 Iniciar servidor de desarrollo

```bash
npm start
```

React iniciará automáticamente en **puerto 3001** (configurado en `.env`)

---

## 🚀 Paso 3: Iniciar los Servidores

### Opción A: Ejecución Manual (Recomendado para desarrollo)

**Terminal 1 - Django Backend:**
```bash
cd d:\ecommerce
.\venv\Scripts\Activate.ps1
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 - React Frontend:**
```bash
cd d:\ecommerce\frontend
npm start
```

Ambos servidores deberían iniciar sin errores.

---

## ✅ Paso 4: Acceder a la Aplicación

### Opción A: Acceso Global (Localhost)
```
http://localhost:3001
```

### Opción B: Acceso por Tenant (Subdominio)
```
http://cliente1.localhost:3001 → Tienda de Tecnología
http://cliente2.localhost:3001 → Boutique de Ropa
```

### Opción C: Acceso por IP (Red Local)
```
http://192.168.56.1:3001
```

---

## 🔐 Credenciales de Prueba

| Usuario | Contraseña | Tenant | Acceso |
|---------|-----------|--------|--------|
| **adm1** | **123** | cliente1 | Tienda de Tecnología |
| **adm2** | **123** | cliente2 | Boutique de Ropa |

**Flujo de Login:**
1. Ingresa credenciales en `/login`
2. Sistema redirige a `/sso` (sincronización de tenant)
3. Accedes al `/dashboard` con tu tienda activa

---

## 🧹 Operaciones de Base de Datos

### Resetear BD completamente
```bash
python reset_db.py
```

### Repoblar BD después de reset
```bash
python seed_db.py
```

### Verificar usuarios en BD
```bash
python check_users.py
```

---

## 🐛 Solución de Problemas

### Error: "Port already in use"

**Liberar puerto 3001:**
```powershell
Get-NetTCPConnection -LocalPort 3001 | Select-Object OwningProcess
taskkill /PID <PID> /F
```

**Liberar puerto 8000:**
```powershell
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
taskkill /PID <PID> /F
```

### Error: "PostgreSQL connection refused"

Verificar:
1. PostgreSQL esté corriendo: `psql --version`
2. Contraseña sea `adm123` en `config/settings.py`
3. BD `mi_saas_db` exista y sea accesible

### Error: "Token inválido en login"

1. Limpiar caché del navegador: `Ctrl + Shift + Del`
2. Hacer logout: `/login` → página
3. Volver a intentar login

### Error: "Credenciales incorrectas después de logout"

Este es un bug conocido que ya fue arreglado en `frontend/src/components/Login.js` línea 26.

---

## 📊 Estructura del Proyecto

```
d:\ecommerce\                    
├── venv/                         # Entorno virtual Python
├── config/                       # Configuración Django
├── customers/                    # Usuarios y Multi-tenancy
├── app_negocio/                  # App de productos
├── manage.py                     # CLI Django
├── seed_db.py                    # Poblar BD 🌱
├── reset_db.py                   # Limpiar BD 🗑️
├── check_users.py                # Verificar usuarios
│
├── frontend/                     # React (puerto 3001)
│   ├── src/
│   │   ├── components/          # Componentes React
│   │   │   ├── Home.js
│   │   │   ├── Login.js
│   │   │   └── Dashboard.jsx
│   │   ├── services/            # API client (Axios)
│   │   ├── contexts/            # Context API (Tenant)
│   │   └── App.js
│   ├── .env                      # Configuración (PORT=3001)
│   └── package.json
│
└── Documentacion/                # Documentación técnica
```

---

## 🔗 URLs Útiles

- **Frontend Home**: `http://localhost:3001`
- **Frontend Login**: `http://localhost:3001/login`
- **Django Admin**: `http://localhost:8000/admin/` (no implementado en UI)
- **Backend API**: `http://localhost:8000/api/`
- **Swagger UI (Documentación Interactiva)**: `http://localhost:8001/api/schema/swagger-ui/` - Prueba endpoints con JWT
- **ReDoc (Documentación)**: `http://localhost:8001/api/schema/redoc/` - Documentación limpia
- **OpenAPI Schema**: `http://localhost:8001/api/schema/` - JSON estándar para importar en Postman
- **Backend Docs**: Ver `Documentacion/`

---

## 📱 Tecnologías Utilizadas

**Backend:**
- Django 6.0.3
- Django REST Framework
- django-tenants (multi-tenancy)
- PostgreSQL
- JWT (djangorestframework-simplejwt)

**Frontend:**
- React 19.2.4
- Axios (HTTP client)
- React Router DOM (enrutamiento)
- Lucide React (iconos)
- TailwindCSS (estilos)

---

## 🚀 Notas Importantes

1. **Puerto 3001**: React corre en 3001, en este local si quieren cambiarlo seria en solo en su local o rama pero no debe aver conflictos en el name 
2. **Multi-tenant**: Soporta acceso por subdominio (`cliente1.localhost`)
3. **SSO**: Login global redirige automáticamente al tenant correspondiente
4. **Rol de Usuario**: Los usuarios creados (adm1, adm2) son superusuarios -- no visible en el dashboard tiene datos mockeados
5. **Datos de Prueba**: `seed_db.py` crea 6 productos de prueba por tenant

---

**¡Proyecto listo para correr! 🎉**