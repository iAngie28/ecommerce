# launcher.py — El Panel de Control del Proyecto

`launcher.py` es el **punto de entrada único** para todo el proyecto. Es un CLI interactivo multiplataforma (Windows, Linux, Mac) que gestiona todos los servicios y operaciones desde un menú.

**Uso:**
```bash
python launcher.py    # desde la raíz del proyecto
```

---

## Mapa de menús

```
launcher.py
│
├── 1 — Iniciar Backend (Django)
│         Activa el venv, corre manage.py runserver en el puerto .env → DJANGO_PORT
│
├── 2 — Iniciar Frontend (React)
│         Busca npm, corre npm start en /frontend en el puerto → REACT_PORT
│
├── A — INICIAR TODO (recomendado)
│         Lanza Backend + Frontend en paralelo con logs entrelazados por colores
│         [BACKEND] en azul   |   [FRONTEND] en cian
│         CTRL+C detiene ambos al mismo tiempo
│
├── 3 — Configuración
│         Ver .env, editar .env, info del proyecto
│
├── 4 — Scripts Útiles
│         Acceso rápido a: db_reset, db_seed, manage_users, test_shell
│
├── 5 — Configuración de Base de Datos
│         Ver/editar configuración DB, probar conexión
│
├── 6 — Gestión de Datos                    ⟵ el más usado en desarrollo
│         1/2. Resetear BD completa
│         3.   Ejecutar seeders (datos de prueba)
│         4.   Ver datos actuales
│         5-7. Crear / Listar / Eliminar usuarios
│         8-9. Migraciones (makemigrations + migrate)
│
├── 7 — Consola de Pruebas
│         Corre test_shell.py interactivo
│
├── 8 — Servicios Nginx                     ⟵ solo en VPS/Linux
│         Crear/gestionar servicios systemd para Django y Frontend
│         Ver estado, logs, recargar, reiniciar, eliminar
│
├── 9 — Sistema
│         Actualizar pip/npm/apt, generar secrets, verificar salud
│
├── 10 — Información del Sistema
└── 0  — Salir
```

---

## Qué hace internamente

### Carga de variables de entorno
Lee el `.env` raíz **sin** depender de `python-dotenv`. Implementación manual en `load_env_manual()`. Extrae `DJANGO_PORT` y `REACT_PORT`.

### Detección del venv
Busca `backend/venv/Scripts/python.exe` (Windows) o `backend/venv/bin/python` (Linux/Mac). Si no existe, lo crea automáticamente.

### Modo INICIAR TODO (opción A)
```python
backend_proc  = Popen([venv_python, 'manage.py', 'runserver', DJANGO_PORT])
frontend_proc = Popen([npm_cmd, 'start'])

# Dos threads leen stdout de cada proceso y lo imprime con prefijo + color
threading.Thread(target=log_output, args=(backend_proc.stdout,  "BACKEND",  BLUE))
threading.Thread(target=log_output, args=(frontend_proc.stdout, "FRONTEND", CYAN))
```
CTRL+C termina los dos procesos y hace cleanup.

### Ejecución de scripts
`run_python_script(nombre, *args)` hace:
1. Cambia el CWD a `/backend` (para que Django encuentre `config.settings`)
2. Añade `/backend` al `PYTHONPATH`
3. Ejecuta el script con el Python del venv

---

## Variables de entorno relevantes (`.env` raíz)

| Variable | Valor por defecto | Descripción |
|----------|------------------|-------------|
| `DJANGO_PORT` | `8001` | Puerto del servidor Django |
| `REACT_PORT` | `3000` | Puerto del servidor React |
| `ENVIRONMENT` | `development` | `development` o `production` |
| `DATABASE_HOST` | `localhost` | Host de PostgreSQL |
| `DATABASE_PORT` | `5432` | Puerto de PostgreSQL |
| `DATABASE_NAME` | — | Nombre de la BD |
| `DATABASE_USER` | — | Usuario de PostgreSQL |
| `DATABASE_PASSWORD` | — | Contraseña de PostgreSQL |
