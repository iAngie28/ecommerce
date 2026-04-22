from customers.services.bitacora_service import BitacoraService

class MultiTenantMixin:
    """
    Filtra los datos para que no se muestren en el esquema 'public'.
    Asegura que cada tenant solo vea su propia información.
    """
    def get_queryset(self):
        from django.db import connection
        
        # Si estamos en el esquema público, no devolvemos nada (seguridad)
        if connection.schema_name == 'public':
            return self.queryset.none()
        
        return super().get_queryset()


class AuditoriaMixin:
    """
    Registra automáticamente las acciones de CREAR, EDITAR y ELIMINAR en la Bitácora.
    Requiere que la vista hija defina el atributo 'modulo_auditoria'.
    """
    modulo_auditoria = None

    def perform_create(self, serializer):
        instancia = serializer.save()
        if self.modulo_auditoria:
            BitacoraService.registrar_accion(
                self.request.user, self.modulo_auditoria, "CREAR",
                request=self.request,
                metadatos={'id': instancia.id}
            )

    def perform_update(self, serializer):
        instancia = serializer.save()
        if self.modulo_auditoria:
            BitacoraService.registrar_accion(
                self.request.user, self.modulo_auditoria, "EDITAR",
                request=self.request,
                metadatos={'id': instancia.id, 'cambios': serializer.initial_data}
            )

    def perform_destroy(self, instance):
        id_instancia = instance.id
        instance.delete()
        if self.modulo_auditoria:
            BitacoraService.registrar_accion(
                self.request.user, self.modulo_auditoria, "ELIMINAR",
                request=self.request,
                metadatos={'id': id_instancia}
            )