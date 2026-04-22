from django.contrib import admin
from .base import TenantSafeAdmin
from ..models import Carrito, CarritoItem


class CarritoItemInline(admin.TabularInline):
    model = CarritoItem
    extra = 0
    readonly_fields = ('fecha_agregado', 'subtotal')
    fields = ('producto', 'cantidad', 'subtotal', 'fecha_agregado')


@admin.register(Carrito)
class CarritoAdmin(TenantSafeAdmin):
    list_display = ('id', 'cliente', 'estado', 'cantidad_items', 'total_carrito', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('cliente__nombre', 'cliente__correo')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'cantidad_items', 'total_carrito')
    inlines = [CarritoItemInline]
    
    fieldsets = (
        ('Información', {
            'fields': ('cliente', 'estado')
        }),
        ('Cálculos', {
            'fields': ('cantidad_items', 'total_carrito')
        }),
        ('Fecha', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
