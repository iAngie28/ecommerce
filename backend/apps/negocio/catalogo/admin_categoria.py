from django.contrib import admin
from apps.negocio.admin.base import TenantSafeAdmin
from ..models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(TenantSafeAdmin):
    list_display = ('nombre', 'parent', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('nombre',)
    readonly_fields = ('fecha_creacion', 'ruta_completa')
    
    fieldsets = (
        ('InformaciÃ³n BÃ¡sica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('JerarquÃ­a', {
            'fields': ('parent', 'ruta_completa')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_creacion')
        }),
    )

