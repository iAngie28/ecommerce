from django.contrib import admin
from .base import PublicOnlyAdmin
from ..models import Cliente


@admin.register(Cliente)
class ClienteAdmin(PublicOnlyAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'nit', 'activo', 'fecha_registro')
    list_filter = ('activo', 'fecha_registro')
    search_fields = ('nombre', 'correo', 'nit')
    readonly_fields = ('fecha_registro', 'id')
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'nombre', 'correo', 'telefono')
        }),
        ('Documentación', {
            'fields': ('nit',)
        }),
        ('Seguridad', {
            'fields': ('contrasena',),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_registro')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['contrasena']
        return self.readonly_fields
