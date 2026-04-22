import os
import shutil
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# --- CONFIGURACIÓN ---
DB_NAME = 'mi_saas_db'
DB_USER = 'postgres'
DB_PASS = 'adm123' #
DB_HOST = '127.0.0.1'
DB_PORT = '5432'

def clean_migrations():
    print("--- 🗑️ Borrando archivos de migraciones (Seguro) ---")
    # Lista de carpetas donde SÍ queremos borrar migraciones
    target_apps = ['customers', 'app_negocio'] 
    
    for app in target_apps:
        migration_dir = os.path.join(app, "migrations")
        if os.path.exists(migration_dir):
            for file in os.listdir(migration_dir):
                # NUNCA borramos __init__.py ni carpetas como __pycache__
                if file != "__init__.py" and os.path.isfile(os.path.join(migration_dir, file)):
                    file_path = os.path.join(migration_dir, file)
                    try:
                        os.remove(file_path)
                        print(f"Eliminado: {file_path}")
                    except Exception as e:
                        print(f"Error eliminando {file_path}: {e}")

def reset_database():
    print(f"--- 🔄 Reiniciando base de datos: {DB_NAME} ---")
    try:
        # Conectar a la base de datos 'postgres' para poder borrar la tuya
        conn = psycopg2.connect(
            dbname='postgres', user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Cerrar conexiones activas para evitar el error "database is being accessed by other users"
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{DB_NAME}'
              AND pid <> pg_backend_pid();
        """)
        
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        
        cursor.close()
        conn.close()
        print("✅ Base de datos recreada con éxito.")
    except Exception as e:
        print(f"❌ Error en la base de datos: {e}")

def run_django_commands():
    print("--- 🏗️ Ejecutando comandos de Django ---")
    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate_schemas --shared")
    # Ejecutamos tu seeder automáticamente al final
    print("--- 🌱 Sembrando datos iniciales ---")
    os.system("python scripts_utiles/seed_db.py")

if __name__ == "__main__":
    clean_migrations()
    reset_database()
    run_django_commands()
    print("\n✨ ¡Todo listo! Sistema reiniciado y datos sembrados.")