from django.contrib import admin
from .base import PublicOnlyAdmin
from ..models import Plan


@admin.register(Plan)
class PlanAdmin(PublicOnlyAdmin):
    list_display = ('nombre', 'precio_mensual', 'precio_anual', 'max_usuarios', 'max_productos', 'activo')
    list_filter = ('activo', 'max_usuarios')
    search_fields = ('nombre',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Precios', {
            'fields': ('precio_mensual', 'precio_anual')
        }),
        ('Límites', {
            'fields': ('max_usuarios', 'max_productos', 'facturacion_max')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
