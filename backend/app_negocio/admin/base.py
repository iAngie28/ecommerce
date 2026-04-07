from django.contrib import admin

class PublicOnlyAdmin(admin.ModelAdmin):
    """Para modelos globales (Client, Domain)."""
    def has_module_permission(self, request):
        return request.tenant.schema_name == 'public'

class TenantSafeAdmin(admin.ModelAdmin):
    """
    Asegura que los datos de una tienda sean invisibles para otra.
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_authenticated or request.user.tenant != request.tenant:
            return qs.none()
        return qs

    def has_add_permission(self, request):
        return request.user.is_authenticated and request.user.tenant == request.tenant

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.tenant == request.tenant

    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.tenant == request.tenant

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.tenant == request.tenant