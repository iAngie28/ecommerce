import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.customers.users.models.permiso import Permiso
from django_tenants.utils import schema_context

with schema_context('public'):
    permisos = [
        {'codigo': 'REP_ESTATICO', 'nombre': 'Reportes Estáticos', 'modulo': 'Reportes', 'es_basico': True, 'descripcion': 'Permite generar y descargar reportes predefinidos'},
        {'codigo': 'REP_DINAMICO', 'nombre': 'Reportes Dinámicos', 'modulo': 'Reportes', 'es_basico': False, 'descripcion': 'Permite armar reportes personalizados con métricas y agrupaciones'},
        {'codigo': 'REP_AUDIO', 'nombre': 'Reportes con IA (Voz)', 'modulo': 'Reportes', 'es_basico': False, 'descripcion': 'Permite realizar consultas al sistema mediante voz o lenguaje natural'},
    ]
    for p in permisos:
        Permiso.objects.get_or_create(codigo=p['codigo'], defaults=p)
    print("OK")
