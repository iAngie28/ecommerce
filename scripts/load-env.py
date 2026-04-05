#!/usr/bin/env python
"""
Script que cargaun variables del .env de la raíz del proyecto
Esto permite que frontend y backend lean del mismo .env centralizado

Uso: 
  python scripts/load-env.py manage.py runserver
  python scripts/load-env.py manage.py migrate
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ruta al .env en la raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / '.env'

if not ENV_FILE.exists():
    print(f"❌ .env no encontrado en: {ENV_FILE}")
    sys.exit(1)

# Cargar variables del .env centralizado
load_dotenv(ENV_FILE)

print(f"✓ Variables de .env cargadas desde: {ENV_FILE}")

# Si hay argumentos, ejecutar comando (ej: manage.py runserver)
if len(sys.argv) > 1:
    # Cambiar al directorio backend
    backend_dir = PROJECT_ROOT / 'backend'
    os.chdir(backend_dir)
    
    # Ejecutar comando
    cmd = sys.argv[1:]
    from django.core.management import execute_from_command_line
    try:
        execute_from_command_line(cmd)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
else:
    print('Variables disponibles:')
    for key in sorted(os.environ.keys()):
        if key.startswith(('DJANGO_', 'DATABASE_', 'REACT_APP_')):
            print(f"  {key}={os.environ[key]}")
