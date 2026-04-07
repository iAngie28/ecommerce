#!/usr/bin/env python
# ========================================================================
# SCRIPT DE MIGRACIONES
# ========================================================================
# Gestiona migraciones de BD
# Uso: python scripts_utiles/migrations.py [comando]

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / 'backend'

def run_make_migrations():
    """Crea nuevas migraciones"""
    os.chdir(BACKEND_DIR)
    subprocess.run([
        sys.executable, 'manage.py', 'makemigrations',
        '--settings=config.settings'
    ])

def run_migrate():
    """Aplica migraciones a la BD"""
    os.chdir(BACKEND_DIR)
    subprocess.run([
        sys.executable, 'manage.py', 'migrate',
        '--settings=config.settings'
    ])

def show_migrations():
    """Muestra estado de migraciones"""
    os.chdir(BACKEND_DIR)
    subprocess.run([
        sys.executable, 'manage.py', 'showmigrations',
        '--settings=config.settings'
    ])

def create_migration(app, name):
    """Crea migración vacía para un app"""
    os.chdir(BACKEND_DIR)
    subprocess.run([
        sys.executable, 'manage.py', 'makemigrations',
        app, '--empty', '--name', name,
        '--settings=config.settings'
    ])

def revert_migration(app, migration):
    """Revierte una migración específica"""
    os.chdir(BACKEND_DIR)
    subprocess.run([
        sys.executable, 'manage.py', 'migrate',
        app, migration,
        '--settings=config.settings'
    ])

def main():
    if len(sys.argv) < 2:
        print("Uso: python migrations.py [comando] [args]")
        print("\nComandos disponibles:")
        print("  make         - Crear nuevas migraciones")
        print("  migrate      - Aplicar migraciones a BD")
        print("  show         - Mostrar estado de migraciones")
        print("  create APP NOMBRE - Crear migración vacía")
        print("  revert APP MIGRATION - Revertir a una migración")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'make':
        run_make_migrations()
    elif cmd == 'migrate':
        run_migrate()
    elif cmd == 'show':
        show_migrations()
    elif cmd == 'create' and len(sys.argv) >= 4:
        create_migration(sys.argv[2], sys.argv[3])
    elif cmd == 'revert' and len(sys.argv) >= 4:
        revert_migration(sys.argv[2], sys.argv[3])
    else:
        print(f"[ERROR] Comando o argumentos inválidos: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    main()
