# ✅ .ENV Centralizado para Frontend y Backend

Todas las configuraciones ahora se leen desde un **único `.env` en la raíz del proyecto**, no desde carpetas individuales de `frontend/` o `backend/`.

---

## 📍 Estructura

```
ecommerce/
├── .env                  ← ARCHIVO ÚNICO Y CENTRAL
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   └── settings_local.py    (Lee de ../.env)
│   └── manage.py
├── frontend/
│   ├── package.json             (Scripts ejecutan load-env.js)
│   └── src/
├── scripts/
│   ├── load-env.js              ← Carga .env para Node
│   └── load-env.py              ← Carga .env para Python
└── launcher.py
```

---

## 🚀 Cómo Usar

### Backend (Django)

**Opción 1: Directamente (recomendado)**
```powershell
cd backend
python manage.py runserver
```
Django automáticamente lee `.env` desde la raíz con el nuevo `settings_local.py`.

**Opción 2: Con script centralizado**
```powershell
python scripts/load-env.py runserver
python scripts/load-env.py migrate
```

---

### Frontend (React)

**Opción 1: npm start (recomendado)**
```powershell
cd frontend
npm start
```
Automáticamente carga `.env` de la raíz y ejecuta `react-scripts start`.

**Opción 2: Especificar variables**
```powershell
cd frontend
REACT_APP_API_URL=http://localhost:8001/api npm start
```

---

## 📋 Variables Disponibles

Variables que React necesita **DEBEN empezar con `REACT_APP_`**:

```env
# .env (raíz)
REACT_APP_API_URL=http://localhost:8001/api
REACT_APP_APP_NAME=Mi SAAS

# Estas automáticamente estarán disponibles en React:
process.env.REACT_APP_API_URL
process.env.REACT_APP_APP_NAME
```

Variables para Backend (Django):

```env
# .env (raíz)
DJANGO_PORT=8001
DJANGO_SECRET_KEY=...
DATABASE_NAME=mi_saas_db
DATABASE_PASSWORD=adm123
```

---

## ⚙️ Cómo Funciona

### Backend (Django)
1. `settings_local.py` carga `.env` desde raíz usando `load_dotenv()`
2. `config()` de decouple lee las variables
3. Django tiene acceso a todas las vars

### Frontend (React)
1. `npm start` ejecuta `node ../scripts/load-env.js react-scripts start`
2. El script JavaScript carga `.env` de raíz y lo pasa como `process.env`
3. Variables con `REACT_APP_` están disponibles en código

---

## 🔒 Seguridad

- **NUNCA** commits `.env` a git (está en `.gitignore`)
- Copia `.env.example` si quieres un template
- En producción, usa variables de sistema operativo en lugar de `.env`

---

## ✅ Verificación

Para ver qué variables se están cargando:

### Backend
```powershell
python scripts/load-env.py
```
Mostrará todas las variables con prefijo `DJANGO_`, `DATABASE_`, `REACT_APP_`

### Frontend
Dentro de tu componente React:
```javascript
console.log(process.env.REACT_APP_API_URL);
```

---

## 🐛 Troubleshooting

**"Cannot find .env"**
- Asegúrate que `.env` esté en la **raíz del proyecto**, no en `backend/` o `frontend/`

**React no ve variables**
- Variables DEBEN empezar con `REACT_APP_` 
- Reinicia `npm start` después de cambiar `.env`

**Django no ve variables**
- Reinicia el servidor Django
- Verifica que `.env` esté en la raíz (no en `backend/`)

