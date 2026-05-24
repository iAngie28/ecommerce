#!/usr/bin/env python
# ========================================================================
# GESTOR DE USUARIOS, ROLES Y PERMISOS V1.0
# ========================================================================
import os
import sys
from pathlib import Path

# ConfiguraciÃ³n de Entorno Django
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from apps.customers.models import Usuario, Rol, Permiso, Client
from django.db import transaction
import re

def validar_password_fuerte(password):
    """Verifica si una contraseÃ±a cumple con los requisitos mÃ­nimos de seguridad"""
    if len(password) < 8:
        return False, "La contraseÃ±a debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", password):
        return False, "Debe incluir al menos una mayÃºscula."
    if not re.search(r"[a-z]", password):
        return False, "Debe incluir al menos una minÃºscula."
    if not re.search(r"\d", password):
        return False, "Debe incluir al menos un nÃºmero."
    if not re.search(r"[@$!%*?&]", password):
        return False, "Debe incluir al menos un carÃ¡cter especial (@$!%*?&)."
    return True, ""

def init_system():
    print("ðŸš€ Inicializando sistema de Roles y Permisos...")
    
    with transaction.atomic():
        # 1. Crear Permisos BÃ¡sicos
        permisos_data = [
            # MÃ³dulo Productos
            ('Ver Productos', 'VER_PRODUCTOS', 'Productos'),
            ('Crear Productos', 'CREAR_PRODUCTOS', 'Productos'),
            ('Editar Productos', 'EDITAR_PRODUCTOS', 'Productos'),
            ('Eliminar Productos', 'ELIMINAR_PRODUCTOS', 'Productos'),
            # MÃ³dulo Ventas
            ('Ver Ventas', 'VER_VENTAS', 'Ventas'),
            ('Gestionar Pedidos', 'GESTIONAR_PEDIDOS', 'Ventas'),
            # MÃ³dulo Usuarios
            ('Ver Usuarios', 'VER_USUARIOS', 'Usuarios'),
            ('Gestionar Roles', 'GESTIONAR_ROLES', 'Usuarios'),
            # MÃ³dulo Sistema
            ('Ver BitÃ¡cora', 'VER_BITACORA', 'Sistema'),
            ('Gestionar Respaldos', 'GESTIONAR_RESPALDOS', 'Sistema'),
        ]

        perms_objs = []
        for nombre, codigo, modulo in permisos_data:
            p, _ = Permiso.objects.get_or_create(
                codigo=codigo, 
                defaults={'nombre': nombre, 'modulo': modulo}
            )
            perms_objs.append(p)
        print(f"  âœ… {len(perms_objs)} permisos sincronizados.")

        # 2. Crear Roles EstÃ¡ndar
        roles_config = [
            ('Super Usuario', 1, 'Acceso total al sistema', perms_objs),
            ('Vendedor', 2, 'GestiÃ³n de tienda y ventas', [p for p in perms_objs if p.modulo in ['Productos', 'Ventas']]),
            ('Cliente', 3, 'Acceso a compras y perfil', [p for p in perms_objs if p.codigo == 'VER_PRODUCTOS']),
        ]

        for nombre, nivel, desc, perms in roles_config:
            rol, _ = Rol.objects.get_or_create(
                nombre=nombre,
                defaults={'nivel': nivel, 'descripcion': desc}
            )
            rol.permisos.set(perms)
            print(f"  âœ… Rol '{nombre}' configurado.")

def set_user_role(email, role_name):
    try:
        user = Usuario.objects.get(email=email)
        rol = Rol.objects.get(nombre__iexact=role_name)
        
        user.roles.add(rol)
        
        # Ajustes de staff segÃºn nivel
        if rol.nivel <= 2:
            user.is_staff = True
        if rol.nivel == 1:
            user.is_superuser = True
            
        user.save()
        print(f"âœ¨ Ã‰XITO: Usuario {email} ahora tiene el rol {rol.nombre}")
    except Usuario.DoesNotExist:
        print(f"âŒ ERROR: No existe usuario con email {email}")
    except Rol.DoesNotExist:
        print(f"âŒ ERROR: El rol '{role_name}' no existe. Usa --init primero.")

def list_users():
    print("\n--- LISTADO DE USUARIOS ---")
    for u in Usuario.objects.all():
        roles = ", ".join([r.nombre for r in u.roles.all()])
        print(f"[{u.id}] {u.email} | Staff: {u.is_staff} | Roles: {roles or 'Ninguno'}")

def create_user(email, password):
    es_fuerte, error = validar_password_fuerte(password)
    if not es_fuerte:
        print(f"âŒ ERROR DE SEGURIDAD: {error}")
        return

    try:
        if Usuario.objects.filter(email=email).exists():
            print(f"âŒ ERROR: El usuario {email} ya existe.")
            return

        user = Usuario.objects.create_user(email=email, password=password)
        print(f"âœ… Usuario {email} creado exitosamente.")
        return user
    except Exception as e:
        print(f"âŒ ERROR al crear usuario: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gestor de Usuarios y Roles")
    parser.add_argument('--init', action='store_true', help="Inicializa roles y permisos bÃ¡sicos")
    parser.add_argument('--list', action='store_true', help="Lista todos los usuarios")
    parser.add_argument('--create', type=str, help="Email del nuevo usuario")
    parser.add_argument('--pass', type=str, dest='password', help="Password del nuevo usuario")
    parser.add_argument('--set-su', type=str, help="Asigna rol Super Usuario a un email")
    parser.add_argument('--set-vendedor', type=str, help="Asigna rol Vendedor a un email")
    parser.add_argument('--set-cliente', type=str, help="Asigna rol Cliente a un email")
    
    args = parser.parse_args()

    if args.init:
        init_system()
    elif args.list:
        list_users()
    elif args.create:
        if not args.password:
            print("âŒ ERROR: Debes proporcionar una contraseÃ±a con --pass")
        else:
            create_user(args.create, args.password)
    elif args.set_su:
        set_user_role(args.set_su, "Super Usuario")
    elif args.set_vendedor:
        set_user_role(args.set_vendedor, "Vendedor")
    elif args.set_cliente:
        set_user_role(args.set_cliente, "Cliente")
    else:
        parser.print_help()

