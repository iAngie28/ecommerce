import os
from django.core.management.base import BaseCommand
from apps.customers.models import Permiso
from django_tenants.utils import schema_context

class Command(BaseCommand):
    help = 'Crea los permisos del sistema (básicos y premium) en el esquema público.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Iniciando Seeder de Permisos ---'))

        # Los permisos siempre se guardan en el esquema público porque 'customers' es SHARED_APP.
        # Nos aseguramos de estar en el public.
        with schema_context('public'):
            
            # Lista de permisos del sistema
            permisos_data = [
                # Módulo Dashboard
                {'codigo': 'VER_DASHBOARD', 'nombre': 'Ver Dashboard', 'modulo': 'Dashboard', 'es_basico': True, 'desc': 'Acceso a la vista principal y métricas básicas'},
                {'codigo': 'VER_DASHBOARD_AVANZADO', 'nombre': 'Dashboard Avanzado', 'modulo': 'Dashboard', 'es_basico': False, 'desc': 'Métricas avanzadas, reportes y predicciones de ventas'},

                # Módulo Productos
                {'codigo': 'CREAR_PRODUCTO', 'nombre': 'Crear Productos', 'modulo': 'Productos', 'es_basico': True, 'desc': 'Permite crear nuevos productos'},
                {'codigo': 'EDITAR_PRODUCTO', 'nombre': 'Editar Productos', 'modulo': 'Productos', 'es_basico': True, 'desc': 'Permite modificar productos existentes'},
                {'codigo': 'ELIMINAR_PRODUCTO', 'nombre': 'Eliminar Productos', 'modulo': 'Productos', 'es_basico': True, 'desc': 'Permite eliminar productos'},
                {'codigo': 'GESTIONAR_INVENTARIO', 'nombre': 'Gestionar Inventario', 'modulo': 'Productos', 'es_basico': True, 'desc': 'Permite gestionar el stock de productos'},

                # Módulo Ventas / Pedidos
                {'codigo': 'VER_PEDIDOS', 'nombre': 'Ver Pedidos', 'modulo': 'Ventas', 'es_basico': True, 'desc': 'Permite listar y ver el detalle de pedidos'},
                {'codigo': 'PROCESAR_PEDIDOS', 'nombre': 'Procesar Pedidos', 'modulo': 'Ventas', 'es_basico': True, 'desc': 'Permite cambiar el estado de los pedidos y registrar envíos'},
                {'codigo': 'EMITIR_FACTURA', 'nombre': 'Emitir Facturas', 'modulo': 'Ventas', 'es_basico': True, 'desc': 'Generación de facturas para ventas'},

                # Módulo Clientes
                {'codigo': 'VER_CLIENTES', 'nombre': 'Ver Clientes', 'modulo': 'Clientes', 'es_basico': True, 'desc': 'Acceso al listado de clientes de la tienda'},
                {'codigo': 'EXPORTAR_CLIENTES', 'nombre': 'Exportar Clientes', 'modulo': 'Clientes', 'es_basico': False, 'desc': 'Permite descargar el padrón de clientes (Feature Premium)'},

                # Módulo Usuarios y Roles (Dueño de la tienda)
                {'codigo': 'GESTIONAR_USUARIOS', 'nombre': 'Gestionar Personal', 'modulo': 'Usuarios', 'es_basico': True, 'desc': 'Permite crear, editar o eliminar empleados/vendedores'},
                {'codigo': 'GESTIONAR_ROLES', 'nombre': 'Gestionar Roles', 'modulo': 'Usuarios', 'es_basico': True, 'desc': 'Permite configurar roles y permisos de los empleados'},

                # Módulo Configuración
                {'codigo': 'CONFIGURACION_TIENDA', 'nombre': 'Configuración de Tienda', 'modulo': 'Configuración', 'es_basico': True, 'desc': 'Permite editar la información de la tienda, logo y colores'},
                {'codigo': 'CONFIGURACION_PAGOS', 'nombre': 'Configuración de Pagos', 'modulo': 'Configuración', 'es_basico': False, 'desc': 'Permite vincular métodos de pago avanzados (Stripe, Paypal)'},

                # Módulo Reportes
                {'codigo': 'REP_ESTATICO', 'nombre': 'Reportes Estáticos', 'modulo': 'Reportes', 'es_basico': True, 'desc': 'Permite generar y descargar reportes predefinidos'},
                {'codigo': 'REP_DINAMICO', 'nombre': 'Reportes Dinámicos', 'modulo': 'Reportes', 'es_basico': False, 'desc': 'Permite armar reportes personalizados con métricas y agrupaciones'},
                {'codigo': 'REP_AUDIO', 'nombre': 'Reportes con IA (Voz)', 'modulo': 'Reportes', 'es_basico': False, 'desc': 'Permite realizar consultas al sistema mediante voz o lenguaje natural'},
            ]

            creados = 0
            actualizados = 0

            for p in permisos_data:
                obj, created = Permiso.objects.update_or_create(
                    codigo=p['codigo'],
                    defaults={
                        'nombre': p['nombre'],
                        'modulo': p['modulo'],
                        'es_basico': p['es_basico'],
                        'descripcion': p['desc'],
                        'activo': True
                    }
                )
                if created:
                    creados += 1
                else:
                    actualizados += 1

            self.stdout.write(self.style.SUCCESS(f'✅ Completado: {creados} permisos creados, {actualizados} permisos actualizados.'))
            self.stdout.write(self.style.WARNING('Nota: Ejecuta este comando en PRODUCCIÓN para habilitar la creación de roles en las tiendas nuevas.'))
