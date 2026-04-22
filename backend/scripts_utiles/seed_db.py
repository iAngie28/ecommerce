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

from customers.models import Client, Domain, Usuario, Rol
from app_negocio.models import Producto, Categoria
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
            'admin_email': 'adm1@admin.com'
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

        # Entramos al contexto del esquema del cliente para crear datos internos
        with schema_context(tenant.schema_name):
            
            # 5. CREACIÓN DE ROLES (Indispensable para el sistema)
            rol_admin, _ = Rol.objects.get_or_create(nombre="Administrador", descripcion="Acceso total")
            Rol.objects.get_or_create(nombre="Vendedor", descripcion="Gestión de ventas y productos")
            Rol.objects.get_or_create(nombre="Cliente", descripcion="Acceso a catálogo y compras")
            print(f"🔑 Roles creados en '{tenant.schema_name}'")

            # 6. CREACIÓN DE USUARIO SUPERVISOR
            if not Usuario.objects.filter(email=data['admin_email']).exists():
                Usuario.objects.create_superuser(
                    email=data['admin_email'],
                    password="123",
                    tenant=tenant,
                    rol=rol_admin # Asignamos el rol creado
                )
                print(f"👤 Superusuario '{data['admin_email']}' creado.")

            # 7. CREACIÓN DE CATEGORÍAS (Para evitar el error de NotNullViolation)
            Producto.objects.all().delete()
            Categoria.objects.all().delete()
            
            if 'Tecnología' in tenant.name:
                cat_principal, _ = Categoria.objects.get_or_create(nombre="Hardware")
                items = [
                    {'nombre': 'Laptop Pro 16"', 'precio': 2500.0, 'stock': 5, 'categoria': cat_principal},
                    {'nombre': 'Mouse Ergonómico', 'precio': 45.0, 'stock': 20, 'categoria': cat_principal},
                ]
            else:
                cat_principal, _ = Categoria.objects.get_or_create(nombre="Vestimenta")
                items = [
                    {'nombre': 'Chaqueta de Cuero', 'precio': 89.99, 'stock': 12, 'categoria': cat_principal},
                    {'nombre': 'Jeans Slim Fit', 'precio': 45.50, 'stock': 30, 'categoria': cat_principal},
                ]
            
            # 8. INSERTAR PRODUCTOS
            for item in items:
                Producto.objects.create(**item)
            
            print(f"📦 Categoría '{cat_principal.nombre}' y productos creados.")

    print("\n--- ✨ Seeder finalizado con éxito ---")

if __name__ == "__main__":
    run_seeder()