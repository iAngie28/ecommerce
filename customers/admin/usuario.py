from django.contrib import admin
from .base import PublicOnlyAdmin
from ..models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(PublicOnlyAdmin):
    list_display = ('username', 'email', 'tenant')