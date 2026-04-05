#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from pathlib import Path

# Configurar rutas
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
FRONTEND_DIR = PROJECT_ROOT / 'frontend'
ENV_PATH = PROJECT_ROOT / '.env'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_step(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}▶ {text}{Colors.RESET}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def create_env():
    print_step("1. Configurando variables de entorno (.env)")
    if ENV_PATH.exists():
        print_success("El archivo .env ya existe. Omitiendo creación.")
        return

    print("Creando archivo .env básico para desarrollo local...")
    # Generar una secret key básica para dev
    import secrets
    secret_key = secrets.token_urlsafe(50)

    env_content = f"""ENVIRONMENT=development
DEBUG=True
DJANGO_SECRET_KEY={secret_key}
DJANGO_PORT=8001
REACT_PORT=3000

# Base de datos (Local por defecto)
DATABASE_NAME=miqhatu_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
"""
    with open(ENV_PATH, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print_success("Archivo .env creado con configuración de desarrollo.")

def setup_backend():
    print_step("2. Configurando Backend (Django)")
    
    if sys.platform == "win32":
        venv_path = BACKEND_DIR / 'venv'
        python_exe = venv_path / 'Scripts' / 'python.exe'
        pip_exe = venv_path / 'Scripts' / 'pip.exe'
    else:
        venv_path = BACKEND_DIR / 'venv'
        python_exe = venv_path / 'bin' / 'python'
        pip_exe = venv_path / 'bin' / 'pip'

    if not venv_path.exists():
        print("Creando entorno virtual (venv)...")
        subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
        print_success("Entorno virtual creado.")
    else:
        print_success("Entorno virtual ya existe.")

    requirements = BACKEND_DIR / 'requirements.txt'
    if requirements.exists():
        print("Instalando dependencias de Python (puede tardar unos minutos)...")
        try:
            subprocess.run([str(pip_exe), 'install', '-r', str(requirements)], cwd=str(BACKEND_DIR), check=True)
            print_success("Dependencias del backend instaladas correctamente.")
        except subprocess.CalledProcessError:
            print_error("Hubo un error instalando las dependencias del backend.")
    else:
        print_error("No se encontró requirements.txt en el backend.")

def setup_frontend():
    print_step("3. Configurando Frontend (React)")
    
    # Buscar npm
    npm_cmd = 'npm.cmd' if sys.platform == "win32" else 'npm'
    
    if not FRONTEND_DIR.exists():
        print_error(f"El directorio frontend no existe: {FRONTEND_DIR}")
        return

    package_json = FRONTEND_DIR / 'package.json'
    if package_json.exists():
        print("Instalando dependencias de Node.js (npm install)...")
        try:
            subprocess.run([npm_cmd, 'install'], cwd=str(FRONTEND_DIR), check=True)
            print_success("Dependencias del frontend instaladas correctamente.")
        except subprocess.CalledProcessError:
            print_error("Hubo un error instalando las dependencias del frontend (npm install).")
    else:
        print_error("No se encontró package.json en el frontend.")

def run_setup():
    print(f"{Colors.BOLD}{Colors.GREEN}=========================================={Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}    ASISTENTE DE INSTALACIÓN RÁPIDA       {Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}=========================================={Colors.RESET}")
    print("Este script configurará el entorno automáticamente para que sea plug & play.")
    
    create_env()
    setup_backend()
    setup_frontend()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}=========================================={Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}    INSTALACIÓN COMPLETADA                {Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}=========================================={Colors.RESET}")
    print("\nPasos siguientes (opcionales pero recomendados):")
    print("1. Revisa tu archivo .env por si necesitas cambiar la contraseña de PostgreSQL.")
    print("2. En el menú, ve a 'Gestión de Datos' -> 'Resetear BD' para inicializar la base de datos.")
    print("3. Selecciona 'Iniciar Todo' para correr el servidor.")
    print()

if __name__ == '__main__':
    run_setup()
