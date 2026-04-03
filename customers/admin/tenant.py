from django.contrib import admin
from .base import PublicOnlyAdmin
from ..models import Client, Domain

@admin.register(Client)
class ClientAdmin(PublicOnlyAdmin):
    list_display = ('schema_name', 'name')

@admin.register(Domain)
class DomainAdmin(PublicOnlyAdmin):
    list_display = ('domain', 'tenant')