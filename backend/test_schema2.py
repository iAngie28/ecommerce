import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.negocio.models import Factura
from apps.customers.models import Client
from django_tenants.utils import schema_context
from apps.negocio.billing.api.serializers import FacturaSerializer

def get_data():
    tenants = Client.objects.exclude(schema_name='public')
    for tenant in tenants:
        with schema_context(tenant.schema_name):
            facturas = Factura.objects.filter(pedido_id=40)
            if facturas.exists():
                serializer = FacturaSerializer(facturas, many=True)
                return serializer.data  # Evaluate inside the with block? Yes!
    return []

try:
    data = get_data()
    print("Success:", data)
except Exception as e:
    import traceback
    traceback.print_exc()
