import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django_tenants.utils import schema_context
from apps.customers.models import Client
from apps.gestionDeUsuarioySeguridad.cu4_gestion_de_roles.models.rol import Rol
from apps.gestionDeUsuarioySeguridad.cu5_gestionar_permisos.models.permiso import Permiso
from apps.gestionDeUsuarioySeguridad.cu3_gestion_de_usuario.models.usuario import Usuario

tenant = Client.objects.exclude(schema_name='public').first()
if tenant:
    with schema_context(tenant.schema_name):
        permisos = Permiso.objects.all()
        for u in Usuario.objects.all():
            for r in u.roles.all():
                r.permisos.add(*permisos)
                print(f"Granted all permissions to role '{r.nombre}' of user '{u.email}'")
        print('All permissions granted successfully.')
else:
    print('No tenant found.')
