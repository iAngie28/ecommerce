from django.contrib import admin
from django.contrib.auth.models import Group
from .base import TenantSafeAdmin

# Desregistramos el Group original para poner el nuestro seguro
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(TenantSafeAdmin):
    filter_horizontal = ('permissions',)