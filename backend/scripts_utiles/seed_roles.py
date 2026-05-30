import os
import sys
import django

# 1. ConfiguraciÃ³n de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.customers.models import Rol, Permiso

def ejecutar():
    print("--- ðŸš€ Iniciando SincronizaciÃ³n de Roles y Permisos ---")

    # 1. Crear Permisos BÃ¡sicos
    permisos_data = [
        # Permisos Super Usuario
        ("Acceso Total Sistema", "SYS_ALL", "Sistema", "Acceso irrestricto a todo el SaaS"),
        ("Gestionar Tenants", "SYS_TENANTS", "Sistema", "Crear y eliminar tiendas"),
        
        # Permisos Vendedor
        ("Gestionar Productos", "STORE_PRODUCTS", "Inventario", "Crear, editar y eliminar productos"),
        ("Gestionar Ventas", "STORE_SALES", "Ventas", "Ver y procesar facturas"),
        ("Ver Reportes", "STORE_REPORTS", "AnÃ¡lisis", "Ver mÃ©tricas de la tienda"),
        
        # Permisos Cliente
        ("Realizar Compras", "CLIENT_BUY", "Tienda", "AÃ±adir al carrito y pagar"),
        ("Ver Historial", "CLIENT_HISTORY", "Tienda", "Ver sus pedidos anteriores"),
    ]

    permisos_creados = {}
    for nombre, codigo, modulo, desc in permisos_data:
        p, created = Permiso.objects.get_or_create(
            codigo=codigo,
            defaults={'nombre': nombre, 'modulo': modulo, 'descripcion': desc, 'activo': True}
        )
        permisos_creados[codigo] = p
        if created:
            print(f"âœ… Permiso creado: {nombre}")

    # 2. Crear Roles
    roles_data = [
        ("super usuario", 1, ["SYS_ALL", "SYS_TENANTS"]),
        ("vendedor", 2, ["STORE_PRODUCTS", "STORE_SALES", "STORE_REPORTS"]),
        ("cliente", 3, ["CLIENT_BUY", "CLIENT_HISTORY"]),
    ]

    for nombre_rol, nivel, codigos_permisos in roles_data:
        rol, created = Rol.objects.get_or_create(
            nombre=nombre_rol,
            defaults={'nivel': nivel, 'descripcion': f"Rol del sistema para {nombre_rol}", 'activo': True}
        )
        if created:
            print(f"âœ… Rol creado: {nombre_rol}")
        
        # Asignar permisos al rol
        permisos_a_asignar = [permisos_creados[codigo] for codigo in codigos_permisos if codigo in permisos_creados]
        rol.permisos.set(permisos_a_asignar)
        print(f"ðŸ”— Permisos asignados a '{nombre_rol}': {len(permisos_a_asignar)}")

    print("\nâœ… SincronizaciÃ³n de Roles finalizada con Ã©xito.")

if __name__ == "__main__":
    ejecutar()

