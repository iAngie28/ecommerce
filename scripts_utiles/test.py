#!/usr/bin/env python
# ========================================================================
# SCRIPT DE TESTING
# ========================================================================
# Ejecuta tests del proyecto
# Uso: python scripts_utiles/test.py [opciones]

import os
import sys
import subprocess
from pathlib import Path

# Directorio raíz
PROJECT_ROOT = Path(__file__).parent.parent

def run_tests():
    """Ejecuta todos los tests"""
    os.chdir(PROJECT_ROOT / 'backend')
    subprocess.run([
        sys.executable, 'manage.py', 'test',
        '--settings=config.settings',
        '--verbosity=2'
    ])

def run_django_tests():
    """Ejecuta solo tests de Django"""
    os.chdir(PROJECT_ROOT / 'backend')
    subprocess.run([
        sys.executable, 'manage.py', 'test',
        'app_negocio', 'customers',
        '--verbosity=2'
    ])

def run_lint():
    """Ejecuta linter (flake8)"""
    print("[+] Ejecutando flake8...")
    subprocess.run([
        sys.executable, '-m', 'flake8',
        str(PROJECT_ROOT / 'backend'),
        '--exclude=venv,migrations',
        '--max-line-length=120'
    ])

def run_migrations_check():
    """Verifica que no hay migraciones pendientes"""
    os.chdir(PROJECT_ROOT / 'backend')
    subprocess.run([
        sys.executable, 'manage.py', 'makemigrations',
        '--dry-run', '--check'
    ])

def main():
    if len(sys.argv) < 2:
        print("Uso: python test.py [comando]")
        print("\nComandos disponibles:")
        print("  all       - Ejecutar todos los tests")
        print("  django    - Ejecutar tests de Django")
        print("  lint      - Ejecutar linter")
        print("  migrations- Verificar migraciones")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'all':
        run_tests()
    elif cmd == 'django':
        run_django_tests()
    elif cmd == 'lint':
        run_lint()
    elif cmd == 'migrations':
        run_migrations_check()
    else:
        print(f"[ERROR] Comando desconocido: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    main()
