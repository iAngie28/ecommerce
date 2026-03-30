import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from customers.models import Client, Domain

# Obtener el tenant público
public_tenant = Client.objects.get(schema_name='public')

# Agregar dominio para la IP
Domain.objects.get_or_create(
    domain='192.168.56.1',
    tenant=public_tenant,
    is_primary=False  # No es el primario
)

print("✅ Dominio '192.168.56.1' agregado al tenant público")

# Listar todos los dominios
all_domains = Domain.objects.all()
print("\n📋 Dominios registrados:")
for domain in all_domains:
    print(f"   - {domain.domain} -> {domain.tenant.schema_name}")
