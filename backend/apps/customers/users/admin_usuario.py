from django.contrib import admin
from apps.customers.admin.base import PublicOnlyAdmin
from ..models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(PublicOnlyAdmin):
    list_display = ('username', 'email', 'tenant')
