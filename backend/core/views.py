from rest_framework import viewsets
from .mixins import AuditoriaMixin

class BaseViewSet(AuditoriaMixin, viewsets.ModelViewSet):
    """
    BaseViewSet que proporciona auditoría automática.
    
    Nota: La multi-tenancia es manejada automáticamente por django-tenants
    a través del middleware.
    """
    pass