import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.negocio.models import Factura
from apps.customers.models import Client
from django_tenants.utils import schema_context

try:
    tenants = Client.objects.exclude(schema_name='public')
    for tenant in tenants:
        with schema_context(tenant.schema_name):
            facturas = Factura.objects.filter(pedido_id=40)
            if facturas.exists():
                print("Factura exists in", tenant.schema_name)
                # simulate serialization
                from apps.negocio.billing.api.serializers import FacturaSerializer
                serializer = FacturaSerializer(facturas, many=True)
                data = serializer.data
                print(data)
except Exception as e:
    import traceback
    traceback.print_exc()
