from django.contrib import admin
from .base import PublicOnlyAdmin
from ..models import Rol


@admin.register(Rol)
class RolAdmin(PublicOnlyAdmin):
    list_display = ('nombre', 'nivel', 'activo', 'descripcion')
    list_filter = ('activo', 'nivel')
    search_fields = ('nombre',)
    ordering = ('nivel',)
