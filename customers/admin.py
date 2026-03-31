from django.contrib import admin
from .models import Client, Domain, Usuario

class PublicOnlyAdmin(admin.ModelAdmin):
    """
    Esta clase hace que el modelo sea INVISIBLE si no estás 
    en el dominio principal (localhost).
    """
    def has_module_permission(self, request):
        # Si el esquema NO es 'public', ocultamos el módulo completo
        if request.tenant.schema_name != 'public':
            return False
        return super().has_module_permission(request)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Solo mostrar datos si estamos en el esquema público
        if request.tenant.schema_name == 'public':
            return qs
        return qs.none()

# --- Registra tus modelos usando esta clase ---

@admin.register(Client)
class ClientAdmin(PublicOnlyAdmin):
    list_display = ('schema_name', 'name')

@admin.register(Domain)
class DomainAdmin(PublicOnlyAdmin):
    list_display = ('domain', 'tenant')

@admin.register(Usuario)
class UsuarioAdmin(PublicOnlyAdmin):
    list_display = ('username', 'email', 'tenant')