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

# ========================================================================
# INICIALIZACIÓN DE DJANGO (Requerido para usar ORM y DB desde afuera)
# ========================================================================
sys.path.insert(0, str(PROJECT_ROOT / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connection, transaction, IntegrityError
from django.db.utils import OperationalError
from customers.models import Client, Usuario  # Ajusta según tu app exacta
# ========================================================================

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

def run_database_connection():
    """Verifica la conexion de la base de datos"""
    print("\n[+] 1/3 Verificando conexión a la base de datos...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
        if row == (1,):
            print("  [OK] La conexion de la base de datos es estable")
        else:
            print("  [ERROR] La BD conectó pero respondió con datos inesperados.")
            sys.exit(1)
    except OperationalError as e:
        print(f"  [ERROR] Fallo la conexion a la base de datos: {e}")
        sys.exit(1)

def run_schema_check():
    """Validar la creación de esquemas (Multi-tenant)"""
    print("\n[+] 2/3 Verificando creación automática de esquemas...")
    test_schema = 'esquema_prueba_qa'
    try:
        # Usamos transaction.atomic para poder deshacer todo al final
        with transaction.atomic():
            # Creamos el tenant
            Client.objects.create(schema_name=test_schema, name="Tenant de Prueba")
            
            # Verificamos directamente en PostgreSQL si el esquema existe
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s;",
                    [test_schema]
                )
                if cursor.fetchone():
                    print(f"  [OK] El esquema '{test_schema}' se creó correctamente en PostgreSQL.")
                else:
                    print(f"  [ERROR] El Tenant se guardó, pero el esquema '{test_schema}' NO se creó.")
                    sys.exit(1)
            
            # Forzamos un rollback para que este tenant de prueba no se guarde en tu BD real
            raise Exception("ROLLBACK_INTENCIONAL")
    except Exception as e:
        if str(e) == "ROLLBACK_INTENCIONAL":
            pass # Todo salió perfecto y limpiamos la BD
        else:
            print(f"  [ERROR] Falló la prueba de esquemas: {e}")
            sys.exit(1)

def run_integrity_check():
    """Verificar la integridad de las tablas (Restricciones UNIQUE, etc)"""
    print("\n[+] 3/3 Verificando integridad de tablas (Restricciones)...")
    try:
        with transaction.atomic():
            tenant = Client.objects.create(schema_name='tenant_integridad', name="Tenant Test")
            
            # 1. Probamos que funcione insertar un usuario normal
            Usuario.objects.create_user(email='unico@test.com', password='123', first_name='Juan', tenant=tenant)
            
            # 2. Forzamos el error de integridad (Mismo correo)
            try:
                # Usamos un savepoint interno para atrapar el error sin romper la transacción principal
                with transaction.atomic(): 
                    Usuario.objects.create_user(email='unico@test.com', password='456', first_name='Pedro', tenant=tenant)
                
                # Si llega aquí, significa que PostgreSQL dejó pasar un correo duplicado
                print("  [ERROR] La base de datos PERMITIÓ guardar un correo duplicado. Revisa tus modelos.")
                sys.exit(1)
            except IntegrityError:
                print("  [OK] La base de datos BLOQUEÓ el correo duplicado correctamente.")
            
            # Limpiamos la BD
            raise Exception("ROLLBACK_INTENCIONAL")
    except Exception as e:
        if str(e) == "ROLLBACK_INTENCIONAL":
            pass
        else:
            print(f"  [ERROR] Falló la prueba de integridad: {e}")
            sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Uso: python test.py [comando]")
        print("\nComandos disponibles:")
        print("  all        - Ejecutar todos los tests (Django)")
        print("  django     - Ejecutar tests de Django")
        print("  lint       - Ejecutar linter")
        print("  migrations - Verificar migraciones")
        print("  sprint1    - Ejecutar los checks de BD, Esquemas e Integridad (Sprint 1)")
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
    elif cmd == 'sprint1':
        # Ejecuta las tres pruebas requeridas en el documento
        run_database_connection()
        run_schema_check()
        run_integrity_check()
        print("\n[OK] Todas las pruebas del Sprint 1 completadas con éxito.")
    else:
        print(f"[ERROR] Comando desconocido: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    main()