from django.shortcuts import render
from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    # El aislamiento por esquema de django-tenants se aplica automáticamente aquí
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer