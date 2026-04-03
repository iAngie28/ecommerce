from django.contrib import admin
from .base import TenantSafeAdmin
from ..models import Producto

@admin.register(Producto)
class ProductoAdmin(TenantSafeAdmin):
    list_display = ('nombre', 'precio', 'stock')
    search_fields = ('nombre',)