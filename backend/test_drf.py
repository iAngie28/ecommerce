import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import RequestFactory
from apps.negocio.billing.api.views import FacturaViewSet

factory = RequestFactory()
request = factory.get('/api/facturas/?pedido=40')
view = FacturaViewSet.as_view({'get': 'list'})

try:
    response = view(request)
    print("Status:", response.status_code)
    print("Data:", response.data)
except Exception as e:
    import traceback
    traceback.print_exc()
