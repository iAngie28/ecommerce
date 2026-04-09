#!/usr/bin/env python
# ========================================================================
# SCRIPT DE SEEDERS - DATOS INICIALES
# ========================================================================
# Carga datos de prueba en BD
# Uso: python scripts_utiles/db_seed.py [opción]

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
import string
from decouple import config

PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

# Cargar el dominio principal desde el entorno (ej: localhost, mi-saas.com, o 157.173.102.129.nip.io)
DOMAIN_MAIN = config('DOMAIN_MAIN', default='localhost')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from customers.models import Client, Usuario, Domain
from app_negocio.models import Producto
from django.contrib.auth.models import User
from django_tenants.utils import tenant_context

def seed_demo():
    """Crea tenant de demostración con datos"""
    print("\n[+] Createando tenant de demostración...")
    
    # Crear tenant
    tenant, created = Client.objects.get_or_create(
        schema_name='demo_company',
        defaults={
            'name': "Demo Company",
        }
    )
    
    if created:
        print(f"[+] Tenant creado: {tenant.name}")
    else:
        print(f"[i] Tenant ya existe: {tenant.name}")
    
    # Crear dominio
    domain, created = Domain.objects.get_or_create(
        domain=f'demo.{DOMAIN_MAIN}',
        defaults={'tenant': tenant}
    )
    
    # Crear usuarios y datos para este tenant
    with tenant_context(tenant):
        admin_email = 'admin@demo.com'
        if not Usuario.objects.filter(email=admin_email).exists():
            admin = Usuario.objects.create_user(
                email=admin_email,
                password='demo123456',
                first_name='Admin',
                last_name='Demo',
                is_staff=True,
                is_active=True
            )
            print(f"[OK] Admin creado: {admin_email}")
        
        # Crear algunos usuarios más
        for i in range(1, 4):
            user_email = f'usuario{i}@demo.com'
            if not Usuario.objects.filter(email=user_email).exists():
                user = Usuario.objects.create_user(
                    email=user_email,
                    password='user123456',
                    first_name=f'Usuario{i}',
                    last_name='Demo',
                    is_active=True
                )
                print(f"[OK] Usuario creado: {user_email}")
        
        # Crear algunos productos de demostración
        demo_products = [
            {'nombre': 'Producto de Prueba A', 'precio': 50.00, 'sku': 'DEMO-001'},
            {'nombre': 'Producto de Prueba B', 'precio': 150.00, 'sku': 'DEMO-002'},
        ]
        for p in demo_products:
            if not Producto.objects.filter(nombre=p['nombre']).exists():
                Producto.objects.create(
                    nombre=p['nombre'],
                    sku=p['sku'],
                    descripcion=f"Este es un producto de prueba para el tenant {tenant.name}",
                    precio=p['precio'],
                    stock=50,
                    categoria='General',
                    activo=True,
                    imagen_url=f"https://picsum.photos/seed/demo_{p['sku']}/400/300"
                )
        print(f"[OK] {len(demo_products)} productos de prueba creados")
    
    print("[OK] Demo seed completado")

def seed_development():
    """Crea ambiente de desarrollo con datos variados"""
    print("\n[+] Creando ambiente de DESARROLLO...")
    
    tenants_count = 3
    users_per_tenant = 5
    products_per_tenant = 10
    
    for t in range(1, tenants_count + 1):
        tenant_name = f"Empresa {t}"
        tenant_slug = f"empresa-{t}"
        schema = f"empresa_{t}"
        
        tenant, created = Client.objects.get_or_create(
            schema_name=schema,
            defaults={
                'name': tenant_name,
            }
        )
        
        if created:
            print(f"  [+] Tenant: {tenant_name}")
            
            # Crear dominio
            Domain.objects.get_or_create(
                domain=f'empresa{t}.localhost',
                defaults={'tenant': tenant}
            )
            
            # Crear usuarios y productos en el contexto del tenant
            with tenant_context(tenant):
                # Crear usuarios
                for u in range(1, users_per_tenant + 1):
                    email = f'user{u}@empresa{t}.local'
                    if not Usuario.objects.filter(email=email).exists():
                        Usuario.objects.create_user(
                            email=email,
                            password='user123456',
                            first_name=f'Usuario{u}',
                            last_name=f'Empresa{t}',
                            is_active=True,  # Todos activos para facilitar pruebas
                            tenant=tenant,   # ← FK al tenant
                        )
                
                print(f"      └─ {users_per_tenant} usuarios")
                
                # Crear productos
                categorias = ['Electrónica', 'Ropa', 'Libros', 'Hogar', 'Deportes', 'Juguetes']
                for p in range(1, products_per_tenant + 1):
                    nombre = f"Producto {p} - {tenant.name}"
                    if not Producto.objects.filter(nombre=nombre).exists():
                        cat = random.choice(categorias)
                        Producto.objects.create(
                            nombre=nombre,
                            sku=f"SKU-{tenant.id}-{p:03d}",
                            descripcion=f"Descripción completa y profesional para el {nombre}. Ideal para pruebas de ecommerce.",
                            precio=round(random.uniform(10, 1000), 2),
                            categoria=cat,
                            stock=random.randint(0, 100),
                            activo=random.choice([True, True, True, False]),  # 75% activos
                            imagen_url=f"https://picsum.photos/seed/{tenant.schema_name}_{p}/400/300"
                        )
                
                print(f"      └─ {products_per_tenant} productos")
        else:
            print(f"  [i] Tenant ya existe: {tenant_name}")
    
    print("[OK] Ambiente de desarrollo creado")

def seed_production_like():
    """Crea ambiente similar a producción (datos más realistas)"""
    print("\n[+] Creando ambiente estilo PRODUCCIÓN...")
    
    # Nombres más realistas
    company_names = [
        "TechStore Martinez",
        "ElectroMundo SA",
        "LibreriaPlus SRL",
        "Fashion Central LTDA"
    ]
    
    for name in company_names:
        slug = name.lower().replace(' ', '-').replace('.', '')
        schema = slug.replace('-', '_')
        
        tenant, created = Client.objects.get_or_create(
            schema_name=schema,
            defaults={
                'name': name,
            }
        )
        
        if created:
            print(f"  [+] Tenant: {name}")
            
            # Dominio basado en nombre
            domain_name = f"{slug}.{DOMAIN_MAIN}"
            Domain.objects.get_or_create(
                domain=domain_name,
                defaults={'tenant': tenant}
            )
            
            with tenant_context(tenant):
                # Admin del tenant
                admin_email = f"admin@{domain_name}"
                if not Usuario.objects.filter(email=admin_email).exists():
                    Usuario.objects.create_user(
                        email=admin_email,
                        password='AdminPassword123!',
                        first_name='Administrador',
                        last_name='General',
                        is_staff=True,
                        is_active=True
                    )
                
                # Varios empleados
                for e in range(1, 4):
                    user_email = f"empleado{e}@{domain_name}"
                    if not Usuario.objects.filter(email=user_email).exists():
                        Usuario.objects.create_user(
                            email=user_email,
                            password='EmpleadoPass123!',
                            first_name=f'Empleado{e}',
                            last_name=name,
                            is_active=True
                        )
                
                print(f"      └─ 1 admin + 3 empleados")
                
                # Productos variados
                products_data = [
                    {'nombre': f'Laptop Premium - {name}', 'precio': 1200, 'stock': 15, 'sku': f'LP-{schema[:3].upper()}-001'},
                    {'nombre': f'Mouse Inalámbrico - {name}', 'precio': 35, 'stock': 100, 'sku': f'MI-{schema[:3].upper()}-002'},
                    {'nombre': f'Teclado Mecánico - {name}', 'precio': 85, 'stock': 45, 'sku': f'TM-{schema[:3].upper()}-003'},
                    {'nombre': f'Monitor 27" - {name}', 'precio': 350, 'stock': 20, 'sku': f'MN-{schema[:3].upper()}-004'},
                    {'nombre': f'Cable USB-C - {name}', 'precio': 15, 'stock': 200, 'sku': f'CB-{schema[:3].upper()}-005'},
                    {'nombre': f'Auriculares Bluetooth - {name}', 'precio': 120, 'stock': 30, 'sku': f'AB-{schema[:3].upper()}-006'},
                    {'nombre': f'Webcam Full HD - {name}', 'precio': 60, 'stock': 25, 'sku': f'WC-{schema[:3].upper()}-007'},
                    {'nombre': f'Hub USB 3.0 - {name}', 'precio': 45, 'stock': 50, 'sku': f'HB-{schema[:3].upper()}-008'},
                ]
                
                for prod in products_data:
                    if not Producto.objects.filter(nombre=prod['nombre']).exists():
                        Producto.objects.create(
                            nombre=prod['nombre'],
                            sku=prod['sku'],
                            descripcion=f"Descripción profesional para {prod['nombre']}. Producto premium importado.",
                            precio=prod['precio'],
                            categoria='Electrónica',
                            stock=prod['stock'],
                            activo=True,
                            imagen_url=f"https://picsum.photos/seed/{schema}_{prod['sku']}/400/300"
                        )
                
                print(f"      └─ {len(products_data)} productos")
        else:
            print(f"  [i] Tenant ya existe: {name}")
    
    print("[OK] Ambiente de producción creado")

def seed_procedural(num_tenants=100, num_users=5, num_products=100):
    """Genera n tenants, cada uno con m usuarios y p productos proceduralmente"""
    print(f"\n[+] Generando ambiente PROCEDURAL:")
    print(f"    - {num_tenants} tenants")
    print(f"    - {num_users} usuarios por tenant")
    print(f"    - {num_products} productos por tenant")
    
    NOMBRES_USUARIOS = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Elena", "Pedro", "Sofia", "Diego", "Laura", "Miguel", "Lucia", "Jorge", "Carmen", "Raul", "Paula", "Andres", "Marta", "Fernando", "Sara"]
    APELLIDOS = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Gomez", "Martin", "Jimenez", "Ruiz", "Hernandez", "Diaz", "Moreno", "Alvarez", "Munoz", "Romero", "Alonso", "Gutierrez"]
    ADJETIVOS_PROD = ["Premium", "Pro", "Max", "Ultra", "Basic", "Plus", "Gamer", "Smart", "Eco", "Classic", "Modern", "Advanced", "Elite", "Original", "Compact", "Lite"]
    TIPOS_PROD = ["Laptop", "Monitor", "Teclado", "Mouse", "Cable", "Auriculares", "Silla", "Escritorio", "Webcam", "Microfono", "Funda", "Mochila", "Tablet", "Celular", "Reloj", "Impresora"]
    CATEGORIAS = ["Electrónica", "Ropa", "Libros", "Hogar", "Deportes", "Juguetes", "Oficina", "Accesorios"]

    # Evitamos colisiones de nombres añadiendo un sufijo
    run_id = random.randint(100, 999)

    for t in range(1, num_tenants + 1):
        tenant_name = f"Procedural Corp {run_id}-{t}"
        schema = f"proc_corp_{run_id}_{t}"
        
        tenant, created = Client.objects.get_or_create(
            schema_name=schema,
            defaults={'name': tenant_name}
        )
        
        if created:
            print(f"  [+] Tenant {t}/{num_tenants}: {tenant_name}")
            Domain.objects.get_or_create(
                domain=f'proc{run_id}a{t}.{DOMAIN_MAIN}',
                defaults={'tenant': tenant}
            )
            
            with tenant_context(tenant):
                # Admin siempre disponible en este tenant
                admin_email = f"admin@{schema}.com"
                if not Usuario.objects.filter(email=admin_email).exists():
                    Usuario.objects.create_user(
                        email=admin_email,
                        password='Password123!',
                        first_name='Admin',
                        last_name=tenant_name,
                        is_staff=True,
                        is_active=True,
                        tenant=tenant
                    )
                
                # Usuarios
                for u in range(1, num_users + 1):
                    email = f"user_{u}_{random.randint(1000,9999)}@{schema}.com"
                    if not Usuario.objects.filter(email=email).exists():
                        Usuario.objects.create_user(
                            email=email,
                            password='Password123!',
                            first_name=random.choice(NOMBRES_USUARIOS),
                            last_name=random.choice(APELLIDOS),
                            is_active=True,
                            tenant=tenant
                        )
                
                # Productos
                productos_creados = 0
                for p in range(1, num_products + 1):
                    tipo = random.choice(TIPOS_PROD)
                    adj = random.choice(ADJETIVOS_PROD)
                    nombre = f"{tipo} {adj} {random.randint(1, 9999)}"
                    sku = f"PRC-{schema[-3:]}-{random.randint(1000,99999)}"
                    if not Producto.objects.filter(sku=sku).exists():
                        try:
                            Producto.objects.create(
                                nombre=nombre,
                                sku=sku,
                                descripcion=f"Descubra el increíble {nombre}. Generado proceduralmente con diseño {adj.lower()}.",
                                precio=round(random.uniform(5.0, 2500.0), 2),
                                categoria=random.choice(CATEGORIAS),
                                stock=random.randint(0, 500),
                                activo=random.choice([True, True, True, False]),
                                imagen_url=f"https://picsum.photos/seed/{sku}/400/300"
                            )
                            productos_creados += 1
                        except Exception:
                            pass
                print(f"      └─ {num_users} usuarios | {productos_creados} productos")
        else:
            print(f"  [i] Tenant ya existe: {tenant_name}")

    print("[OK] Ambiente procedural completado")

def show_seeds():
    """Muestra opciones de seeds disponibles"""
    print("\n" + "="*60)
    print("SEMILLAS (SEEDERS) DISPONIBLES")
    print("="*60)
    print("\nOpciones:")
    print("  1. Demo         - Tenant único de prueba")
    print("  2. Development  - 3 tenants con datos variados")
    print("  3. Production   - Empresas realistas con datos profesionales")
    print("  4. Procedural   - N registros por tabla generados al azar")
    print("")

def main():
    if len(sys.argv) < 2:
        show_seeds()
        cmd = input(f"  ? Selecciona: ").strip().lower()
        if not cmd:
            print("[INFO] Operación cancelada")
            return
    else:
        cmd = sys.argv[1]
    
    if cmd == '1' or cmd == 'demo':
        seed_demo()
    elif cmd == '2' or cmd == 'dev':
        seed_development()
    elif cmd == '3' or cmd == 'prod':
        seed_production_like()
    elif cmd == '4' or cmd == 'procedural':
        try:
            num_tenants = input("  ¿Cuántos tenants generar? (ej: 100): ").strip()
            num_tenants = int(num_tenants) if num_tenants else 100
            
            num_users = input("  ¿Cuántos usuarios por cada tenant? (ej: 5): ").strip()
            num_users = int(num_users) if num_users else 5
            
            num_products = input("  ¿Cuántos productos por cada tenant? (ej: 100): ").strip()
            num_products = int(num_products) if num_products else 100
        except ValueError:
            print("  [WARN] Cantidad inválida ingresada. Cancelando.")
            return

        seed_procedural(num_tenants, num_users, num_products)
    elif cmd == 'list':
        show_seeds()
    else:
        print(f"[ERROR] Comando desconocido: {cmd}")
        sys.exit(1)
    
    print("\n[OK] Completado")

if __name__ == '__main__':
    main()
