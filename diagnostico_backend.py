import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
from customers.models import Usuario, Client

print("\n" + "="*60)
print("🔍 DIAGNÓSTICO: PROBLEMA DE LOGIN POST-LOGOUT")
print("="*60)

# 1. Verificar usuarios
print("\n1️⃣ USUARIOS EN BD:")
usuarios = Usuario.objects.all()
print(f"Total: {usuarios.count()}")
for user in usuarios:
    print(f"   - {user.username} | Email: {user.email} | Tenant: {user.tenant}")

# 2. Verificar tenants
print("\n2️⃣ TENANTS (CLIENTES):")
tenants = Client.objects.all()
for tenant in tenants:
    print(f"   - {tenant.schema_name} | {tenant.name}")

# 3. Test de autenticación
print("\n3️⃣ TEST DE AUTENTICACIÓN:")
print("   Intentando autenticar adm1/123...")
user = authenticate(username='adm1', password='123')
if user:
    print(f"   ✓ Autenticación exitosa: {user.username}")
    print(f"     - ID: {user.id}")
    print(f"     - Tenant: {user.tenant}")
    print(f"     - Is Active: {user.is_active}")
else:
    print("   ❌ Autenticación FALLÓ")

# 4. Test directo en BD
print("\n4️⃣ BÚSQUEDA DIRECTA EN BD:")
try:
    adm1 = Usuario.objects.get(username='adm1')
    print(f"   ✓ Usuario encontrado: {adm1.username}")
    print(f"     - Password válida: {adm1.check_password('123')}")
    print(f"     - Is Active: {adm1.is_active}")
    print(f"     - Tenant: {adm1.tenant}")
except Usuario.DoesNotExist:
    print("   ❌ Usuario 'adm1' NO EXISTE en BD")

# 5. Endpoints disponibles
print("\n5️⃣ VERIFICAR TOKENS JWT:")
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

try:
    adm1 = Usuario.objects.get(username='adm1')
    refresh = RefreshToken.for_user(adm1)
    access = str(refresh.access_token)
    print(f"   ✓ Tokens generados correctamente")
    print(f"   Access token (primer 50 chars): {access[:50]}...")
    print(f"   Refresh token (primer 50 chars): {str(refresh)[:50]}...")
except Exception as e:
    print(f"   ❌ Error generando tokens: {e}")

print("\n" + "="*60)
print("✅ DIAGNÓSTICO COMPLETADO")
print("="*60 + "\n")
