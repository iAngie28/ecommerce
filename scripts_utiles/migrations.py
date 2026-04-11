#!/usr/bin/env python
# ========================================================================
# SCRIPT DE MIGRACIONES (GENÉRICO Y RECURSIVO)
# ========================================================================
# Gestiona migraciones de BD detectando cambios automáticamente
# Uso: python scripts_utiles/migrations.py [comando]

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / 'backend'

def run_make_migrations():
    """Crea nuevas migraciones detectando cambios recursivamente"""
    print("\n[+] Buscando cambios en modelos...")
    os.chdir(BACKEND_DIR)
    subprocess.run([
        sys.executable, 'manage.py', 'makemigrations',
        '--settings=config.settings'
    ])

def run_migrate():
    """Aplica migraciones al esquema público (Shared Apps)"""
    print("\n[+] Aplicando migraciones al esquema público (SHARED)...")
    os.chdir(BACKEND_DIR)
    subprocess.run([
        sys.executable, 'manage.py', 'migrate',
        '--settings=config.settings'
    ])

def run_migrate_schemas():
    """Aplica migraciones a todos los esquemas de clientes (Tenants)"""
    print("\n[+] Aplicando migraciones a todos los TENANTS...")
    os.chdir(BACKEND_DIR)
    # django-tenants usa migrate_schemas para las TENANT_APPS
    subprocess.run([
        sys.executable, 'manage.py', 'migrate_schemas',
        '--settings=config.settings'
    ])

def run_full_sync():
    """Ejecuta el ciclo completo de sincronización de base de datos"""
    print("\n" + "="*60)
    print("SINCRONIZACIÓN TOTAL DE BASE DE DATOS")
    print("="*60)
    run_make_migrations()
    run_migrate()
    run_migrate_schemas()
    print("\n[OK] Base de datos sincronizada correctamente.")

def show_migrations():
    """Muestra estado de migraciones"""
    os.chdir(BACKEND_DIR)
    subprocess.run([
        sys.executable, 'manage.py', 'showmigrations',
        '--settings=config.settings'
    ])

def main():
    if len(sys.argv) < 2:
        print("Uso: python migrations.py [comando] [args]")
        print("\nComandos disponibles:")
        print("  sync         - Sincronización TOTAL (Make + Migrate Shared + Migrate Tenants)")
        print("  make         - Crear nuevas migraciones")
        print("  migrate      - Aplicar migraciones al esquema público")
        print("  tenants      - Aplicar migraciones a los esquemas de clientes")
        print("  show         - Mostrar estado de migraciones")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'sync':
        run_full_sync()
    elif cmd == 'make':
        run_make_migrations()
    elif cmd == 'migrate':
        run_migrate()
    elif cmd == 'tenants':
        run_migrate_schemas()
    elif cmd == 'show':
        show_migrations()
    else:
        print(f"[ERROR] Comando o argumentos inválidos: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    main()
