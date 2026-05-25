import os, django
from dotenv import load_dotenv
load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()
from django_tenants.utils import schema_context
from apps.negocio.models import Pedido

try:
    with schema_context('sony'):
        p = Pedido.objects.get(id=4)
        for i in p.carrito.items.all():
            print(f"Producto: {i.producto.nombre}, Cantidad: {i.cantidad}")
except Exception as e:
    print(e)
