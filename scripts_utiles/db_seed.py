#!/usr/bin/env python
# ========================================================================
# SCRIPT DE SEEDERS - GENERACIÓN PROCEDURAL DE NEGOCIO
# ========================================================================
# Genera datos de prueba coherentes (Usuarios, Productos, Bitácora)
# Uso: python scripts_utiles/db_seed.py [opción]

import os
import sys
import random
import string
from pathlib import Path
from datetime import datetime, timedelta
from django.utils import timezone
from decouple import config

PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.apps import apps
from django.db import models
from django_tenants.utils import tenant_context, schema_context
from customers.models import Client, Domain, Usuario, Bitacora
from customers.services.bitacora_service import BitacoraService
from app_negocio.models import Producto

# ========================================================================
# GENERADOR DE NEGOCIO (COHERENTE)
# ========================================================================
class BusinessGenerator:
    PASSWORD_STANDAR = "Password123!"
    
    MODULOS = ["Autenticación", "Productos", "Tiendas", "Usuarios", "Inventario"]
    ACCIONES = ["LOGIN", "CREAR", "EDITAR", "ELIMINAR", "VER_DETALLE", "LOGOUT"]
    
    # Listas ampliadas por el usuario
    IPS_TEST = [
        "192.168.1.10", "185.22.44.1", "10.0.0.5", "172.16.8.20", "8.8.8.8", "1.1.1.1",
        "127.0.0.1", "203.0.113.50", "198.51.100.14", "104.21.55.2"
    ]

    BROWSERS = [
        "Chrome/120.0.0.0", "Firefox/121.0.1", "Safari/17.2", "Edge/119.0.0",
        "Opera/102.0.4880.56", "Brave/1.57.62"
    ]

    NOMBRES_REALS = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Elena", "Pedro", "Sofia", "Diego", "Laura", "Mateo", "German", "Alejandro", "Dexter"]
    APELLIDOS_REALS = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Gomez", "Martin"]

    PROD_TIPOS = ["Laptop", "Monitor", "Teclado", "Mouse", "Impresora", "Tablet", "Celular", "Smartwatch", "Audifonos"]
    PROD_MARCAS = ["TechX", "Quantum", "Nexus", "Elite", "ProMax", "Cyber", "Mega", "Ultra", "Hyper"]

    @staticmethod
    def random_user_data(index, tenant_schema):
        nombre = random.choice(BusinessGenerator.NOMBRES_REALS)
        apellido = random.choice(BusinessGenerator.APELLIDOS_REALS)
        email = f"user{index}@{tenant_schema}.local"
        return {
            'email': email,
            'password': BusinessGenerator.PASSWORD_STANDAR,
            'first_name': nombre,
            'last_name': apellido,
            'is_active': True
        }

    @staticmethod
    def random_product_data(index):
        tipo = random.choice(BusinessGenerator.PROD_TIPOS)
        marca = random.choice(BusinessGenerator.PROD_MARCAS)
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        nombre = f"{tipo} {marca}-{index:03d}"
        return {
            'nombre': nombre,
            'sku': f"SKU-{marca[:2].upper()}-{index:04d}-{suffix}",
            'precio': round(random.uniform(50.0, 2000.0), 2),
            'stock': random.randint(5, 100),
            'categoria': 'General',
            'activo': True,
            'descripcion': f"Descripción detallada del {nombre}. Producto de prueba generado proceduralmente."
        }

    @staticmethod
    def random_audit_event_data(modulo=None, accion=None):
        """Genera datos para un evento, sin el objeto usuario aún."""
        return {
            'modulo': modulo or random.choice(BusinessGenerator.MODULOS),
            'accion': accion or random.choice(BusinessGenerator.ACCIONES),
            'ip': random.choice(BusinessGenerator.IPS_TEST),
            'browser': random.choice(BusinessGenerator.BROWSERS),
            'metadatos': {'status': 'seeded', 'gen': 'procedural'}
        }

# ========================================================================
# MOTOR DE SEEDING INTERACTIVO
# ========================================================================

class DatabaseSeeder:
    def __init__(self):
        self.credentials_report = []

    def print_report(self):
        print("\n" + "="*80)
        print(f"{'REPORTE DE ACCESOS (CREADOS O EXISTENTES)':^80}")
        print("="*80)
        print(f"{'SCHEMA':<15} | {'USUARIO (EMAIL)':<40} | {'PASSWORD'}")
        print("-" * 80)
        for cred in self.credentials_report:
            print(f"{cred['schema']:<15} | {cred['email']:<40} | {cred['password']}")
        print("="*80)
        print("\n[TIP] Usa estas credenciales para entrar a los respectivos subdominios.")

    def seed_tenants(self, count, u_range, p_range):
        from django.conf import settings
        
        # Obtener el sufijo del dominio desde settings (respeta el .env)
        suffix = getattr(settings, 'TENANT_DOMAIN_SUFFIX', '.localhost')
        if not suffix.startswith('.') and suffix != 'localhost':
            suffix = f".{suffix}"
            
        print(f"\n[+] Iniciando generacion de {count} tenants...")
        print(f"[i] Usando sufijo de dominio: {suffix}")
        
        for i in range(1, count + 1):
            # USAMOS 'x' como separador alfanumérico para evitar guiones y guiones bajos (Problemas DNS)
            schema = f"tiendax{i}"
            name = f"Mi Tienda {i}"
            # Usamos el mismo nombre para el subdominio
            domain_name = f"tiendax{i}{suffix}"

            # Operaciones de Tenant en el esquema publico (CORE de django-tenants)
            with schema_context('public'):
                tenant, created = Client.objects.get_or_create(
                    schema_name=schema, 
                    defaults={'name': name}
                )
                Domain.objects.get_or_create(domain=domain_name, tenant=tenant)
                print(f"\n  [Paso {i}/{count}] Poblando: {schema} ({domain_name})...")

            with tenant_context(tenant):
                admin_email = f"admin@{schema}.local"
                
                # Aseguramos contexto publico para el Usuario (Shared Model)
                with schema_context('public'):
                    admin_data = BusinessGenerator.random_user_data(0, schema)
                    admin_data['email'] = admin_email
                    if not Usuario.objects.filter(email=admin_email).exists():
                        admin = Usuario.objects.create_user(**admin_data)
                    else:
                        admin = Usuario.objects.get(email=admin_email)
                    
                    # Siempre añadir al reporte para que el usuario sepa con qué entrar
                    self.credentials_report.append({
                        'schema': schema,
                        'email': admin_email,
                        'password': admin_data['password']
                    })

                # 2. Crear Usuarios (Shared Model, contexto publico)
                num_users = random.randint(u_range[0], u_range[1])
                with schema_context('public'):
                    for u in range(1, num_users + 1):
                        u_data = BusinessGenerator.random_user_data(u, schema)
                        if not Usuario.objects.filter(email=u_data['email']).exists():
                            Usuario.objects.create_user(**u_data)
                print(f"    - {num_users} usuarios adicionales creados en public.")

                # 3. Crear Productos (Tenant Model, contexto de tienda)
                num_prods = random.randint(p_range[0], p_range[1])
                for p in range(1, num_prods + 1):
                    p_data = BusinessGenerator.random_product_data(p)
                    Producto.objects.create(**p_data)
                print(f"    - {num_prods} productos creados en {schema}.")

                # 4. Crear Histórico de Bitácora (Shared Model, contexto publico)
                print(f"    - Generando historico de auditoria...")
                with schema_context('public'):
                    # Simular flujo: Login -> 3 acciones -> Logout
                    # Usamos el servicio directamente para asegurar IP y metadatos
                    
                    # Login
                    ev = BusinessGenerator.random_audit_event_data("Autenticación", "LOGIN")
                    BitacoraService.registrar(admin, ev['modulo'], ev['accion'], metadatos={'ip': ev['ip'], 'browser': ev['browser']})
                    
                    # Acciones
                    for _ in range(3):
                        ev = BusinessGenerator.random_audit_event_data()
                        BitacoraService.registrar(admin, ev['modulo'], ev['accion'], metadatos={'ip': ev['ip'], 'browser': ev['browser']})
                    
                    # Logout
                    ev = BusinessGenerator.random_audit_event_data("Autenticación", "LOGOUT")
                    BitacoraService.registrar(admin, ev['modulo'], ev['accion'], metadatos={'ip': ev['ip'], 'browser': ev['browser']})
                
                print(f"    - Historial de bitacora guardado en public para {admin.email}.")

        print("\n[OK] Generacion procedimental finalizada.")

def parse_quantity(user_input, default_min, default_max=None):
    """
    Parsea la entrada del usuario para soportar:
    - Exacta: "5" -> (5, 5)
    - Rango: "2-10" -> (2, 10)
    - Default: "" -> (default_min, default_max)
    """
    val = user_input.strip()
    if not val:
        return (default_min, default_max or default_min)
    
    if '-' in val:
        try:
            parts = val.split('-')
            low = int(parts[0])
            high = int(parts[1])
            return (min(low, high), max(low, high))
        except ValueError:
            print(f"  [!] Rango invalido '{val}', usando default {default_min}-{default_max}")
            return (default_min, default_max or default_min)
    else:
        try:
            num = int(val)
            return (num, num)
        except ValueError:
            print(f"  [!] Cantidad invalida '{val}', usando default {default_min}")
            return (default_min, default_max or default_min)

def main():
    print("\n" + "="*70)
    print(f"{'MOTOR DE GENERACIÓN PROCEDURAL (V3.0)':^70}")
    print("="*70)
    print(" Soporta: Cantidad exacta (ej: 5), Rangos (ej: 2-10) o Default (Enter)")
    
    try:
        # 1. Tenants
        t_input = input("\n  1. ¿Cuantos Tenants/Tiendas? [Default 2]: ")
        t_min, t_max = parse_quantity(t_input, 2, 2)
        t_count = random.randint(t_min, t_max)
        
        # 2. Usuarios
        u_input = input("  2. ¿Usuarios por tienda? (ej: 5 o 2-8) [Default 3-8]: ")
        u_range = parse_quantity(u_input, 3, 8)
        
        # 3. Productos
        p_input = input("  3. ¿Productos por tienda? (ej: 20 o 10-30) [Default 10-20]: ")
        p_range = parse_quantity(p_input, 10, 20)
        
        print("\n" + "-"*70)
        print(f" CONFIGURACIÓN: {t_count} tiendas | {u_range[0]}-{u_range[1]} users | {p_range[0]}-{p_range[1]} prods")
        print("-" * 70)
        
        seeder = DatabaseSeeder()
        seeder.seed_tenants(t_count, u_range, p_range)
        seeder.print_report()
        
    except KeyboardInterrupt:
        print(f"\n[!] Operacion cancelada por el usuario.")
    except Exception as e:
        import traceback
        print(f"\n[ERROR] Ocurrio un fallo en el seeding: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    main()
