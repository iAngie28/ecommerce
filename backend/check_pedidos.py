import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django_tenants.utils import schema_context
from apps.customers.models import Client
from apps.negocio.models import Pedido

tenants = Client.objects.all()
for t in tenants:
    with schema_context(t.schema_name):
        pedidos = Pedido.objects.all()
        for p in pedidos:
            print(f"[{t.schema_name}] Pedido {p.id} - Estado: {p.estado} - Cliente: {p.carrito.cliente.correo if p.carrito else 'No_Carrito'}")
