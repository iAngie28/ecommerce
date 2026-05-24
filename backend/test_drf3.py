import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import RequestFactory
from apps.negocio.billing.api.views import FacturaViewSet
from apps.customers.models import Usuario
from rest_framework.test import force_authenticate

factory = RequestFactory()
request = factory.get('/api/facturas/?pedido=40')
request.META['HTTP_HOST'] = '192.168.100.244:8001' # force public schema via middleware simulation if needed

user = Usuario.objects.filter(email="test@gmail.com").first()

view = FacturaViewSet.as_view({'get': 'list'})
force_authenticate(request, user=user)

try:
    response = view(request)
    print("Status:", response.status_code)
    print("Data:", response.data)
except Exception as e:
    import traceback
    traceback.print_exc()
