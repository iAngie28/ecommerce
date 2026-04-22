import os
import sys
import django
from pathlib import Path

# 1. AJUSTE DE RUTAS
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
sys.path.append(str(BACKEND_DIR))

# 2. Configuración del entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from customers.models import Client, Domain, Usuario
from app_negocio.models import Producto
from django_tenants.utils import schema_context

def run_seeder():
    print("--- 🚀 Iniciando Seeder Multi-tenant corregido ---")

    # 3. Esquema Público
    public_tenant, _ = Client.objects.get_or_create(
        schema_name='public', 
        defaults={'name': 'Plataforma Global'}
    )
    Domain.objects.get_or_create(
        domain='localhost', 
        tenant=public_tenant, 
        defaults={'is_primary': True}
    )
    print("✅ Dominio 'localhost' listo.")

    # 4. Datos de los Clientes
    tenants_data = [
        {
            'schema': 'cliente1', 
            'name': 'Tienda de Tecnología', 
            'domain': 'cliente1.localhost', 
            'admin_email': 'adm1@admin.com' # Usamos email como ID
        },
        {
            'schema': 'cliente2', 
            'name': 'Boutique de Ropa', 
            'domain': 'cliente2.localhost', 
            'admin_email': 'adm2@admin.com'
        },
    ]

    for data in tenants_data:
        print(f"\n⚙️ Procesando: {data['name']}...")
        
        tenant, _ = Client.objects.get_or_create(
            schema_name=data['schema'], 
            defaults={'name': data['name']}
        )
        
        Domain.objects.get_or_create(
            domain=data['domain'], 
            tenant=tenant, 
            defaults={'is_primary': True}
        )

        # 5. CREACIÓN DE USUARIO (CORREGIDO: usando email)
        if not Usuario.objects.filter(email=data['admin_email']).exists():
            Usuario.objects.create_superuser(
                email=data['admin_email'],
                password="123",
                tenant=tenant 
            )
            print(f"👤 Superusuario '{data['admin_email']}' creado.")

        # 6. Crear Productos dentro del esquema
        with schema_context(tenant.schema_name):
            Producto.objects.all().delete()
            
            if 'Tecnología' in tenant.name:
                items = [
                    {'nombre': 'Laptop Pro 16"', 'precio': 2500.0, 'stock': 5},
                    {'nombre': 'Mouse Ergonómico', 'precio': 45.0, 'stock': 20},
                ]
            else:
                items = [
                    {'nombre': 'Chaqueta de Cuero', 'precio': 89.99, 'stock': 12},
                    {'nombre': 'Jeans Slim Fit', 'precio': 45.50, 'stock': 30},
                ]
            
            for item in items:
                Producto.objects.create(**item)
            
            print(f"📦 Productos insertados en '{tenant.schema_name}'")

    print("\n--- ✨ Seeder finalizado ---")

if __name__ == "__main__":
    run_seeder()