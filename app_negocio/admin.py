from django.contrib import admin
from .models import Producto  # Supongamos que agregas estas
from django.contrib.auth.models import Group


class TenantSafeAdmin(admin.ModelAdmin):
    """
    Clase Maestra de Seguridad: 
    Cualquier admin que herede de aquí será invisible para usuarios de otros tenants.
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filtro de lectura: Si el usuario no es del tenant actual, lista vacía.
        if request.user.tenant != request.tenant:
            return qs.none()
        return qs

    def has_add_permission(self, request):
        return request.user.tenant == request.tenant

    def has_change_permission(self, request, obj=None):
        return request.user.tenant == request.tenant

    def has_delete_permission(self, request, obj=None):
        return request.user.tenant == request.tenant

    def has_view_permission(self, request, obj=None):
        return request.user.tenant == request.tenant

# Quitamos el registro por defecto y ponemos el nuestro con seguridad
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(TenantSafeAdmin): # <--- Usamos la misma base de seguridad que creamos
    """
    Evita que el adm1 cree grupos que el adm2 pueda ver o usar.
    """
    filter_horizontal = ('permissions',) # Para que sea más fácil asignar permisos

# --- Ahora registrar tus tablas es súper fácil y seguro ---

@admin.register(Producto)
class ProductoAdmin(TenantSafeAdmin): # <--- Hereda seguridad
    list_display = ('nombre', 'precio', 'stock')
