import os
import django

# 1. Configuración del entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from customers.models import Client, Domain, Usuario
from app_negocio.models import Producto
from django_tenants.utils import schema_context

def run_seeder():
    print("--- 🚀 Iniciando Seeder Multi-tenant (Localhost) ---")

    # 2. Esquema Público
    print("Configurando esquema público...")
    public_tenant, _ = Client.objects.get_or_create(
        schema_name='public', 
        name='Plataforma Global'
    )
    Domain.objects.get_or_create(
        domain='localhost', 
        tenant=public_tenant, 
        is_primary=True
    )
    print("✅ Dominio base 'localhost' registrado.")

    # 3. Datos de los Clientes
    tenants_data = [
        {
            'schema': 'cliente1', 
            'name': 'Tienda de Tecnología', 
            'domain': 'cliente1.localhost', # Volvemos a .localhost
            'custom_user': 'adm1'
        },
        {
            'schema': 'cliente2', 
            'name': 'Boutique de Ropa', 
            'domain': 'cliente2.localhost', # Volvemos a .localhost
            'custom_user': 'adm2'
        },
    ]

    for data in tenants_data:
        print(f"\n⚙️ Procesando: {data['name']}...")
        
        # Crear el Cliente
        tenant, _ = Client.objects.get_or_create(
            schema_name=data['schema'], 
            name=data['name']
        )
        
        # Crear el Dominio
        Domain.objects.get_or_create(
            domain=data['domain'], 
            tenant=tenant, 
            is_primary=True
        )

        # 4. Crear Usuario con el nombre solicitado
        if not Usuario.objects.filter(username=data['custom_user']).exists():
            Usuario.objects.create_superuser(
                username=data['custom_user'],
                email=f"admin@{data['schema']}.com",
                password="123",
                tenant=tenant 
            )
            print(f"👤 Usuario '{data['custom_user']}' creado.")

        # 5. Crear Productos
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