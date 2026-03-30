import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from customers.models import Usuario

usuarios = Usuario.objects.all()
print(f"\n=== Total usuarios en BD: {usuarios.count()} ===")
for user in usuarios:
    print(f"- Username: {user.username}, Tenant: {user.tenant}, Email: {user.email}")

if usuarios.count() == 0:
    print("\n⚠️ No hay usuarios. Creando usuarios de prueba...")
    from customers.models import Client
    
    # Crear usuarios manualmente
    tenants_data = [
        {'schema': 'cliente1', 'custom_user': 'adm1'},
        {'schema': 'cliente2', 'custom_user': 'adm2'},
    ]
    
    for data in tenants_data:
        try:
            tenant = Client.objects.get(schema_name=data['schema'])
            Usuario.objects.create_superuser(
                username=data['custom_user'],
                email=f"admin@{data['schema']}.com",
                password="123",
                tenant=tenant
            )
            print(f"✅ Usuario '{data['custom_user']}' creado exitosamente")
        except Exception as e:
            print(f"❌ Error creando '{data['custom_user']}': {e}")
