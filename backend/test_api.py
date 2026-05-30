import os
import django
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.customers.models import Cliente
from apps.negocio.ordenes.api.pedido_views import PedidoViewSet
from rest_framework.test import force_authenticate

factory = RequestFactory()
request = factory.get('/api/pedidos/global-list/')
cliente = Cliente.objects.first()
if not cliente:
    print("Cliente not found")
else:
    request.user = cliente 
    request.user.email = cliente.correo
    view = PedidoViewSet.as_view({'get': 'global_list'})
    force_authenticate(request, user=cliente)
    response = view(request)
    print(response.status_code)
    print(response.data)
