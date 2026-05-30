import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django_tenants.utils import schema_context
from apps.negocio.models import Pedido
from apps.negocio.ordenes.api.pedido_serializer import PedidoSerializer

with schema_context('sony'):
    pedidos = Pedido.objects.all()
    serializer = PedidoSerializer(pedidos, many=True)
    print(json.dumps(serializer.data, indent=2))
