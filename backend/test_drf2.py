import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import RequestFactory
from apps.negocio.billing.api.views import FacturaViewSet
from apps.customers.models import Cliente
from rest_framework.test import force_authenticate

factory = RequestFactory()
request = factory.get('/api/facturas/?pedido=40')
request.META['HTTP_HOST'] = '192.168.100.244:8001' # force public schema via middleware simulation if needed

user = Cliente.objects.filter(correo="qqqq@gmail.com").first()

view = FacturaViewSet.as_view({'get': 'list'})
from rest_framework.request import Request
drf_request = Request(request)
force_authenticate(drf_request, user=user)

try:
    response = view(drf_request)
    print("Status:", response.status_code)
    print("Data:", response.data)
except Exception as e:
    import traceback
    traceback.print_exc()
