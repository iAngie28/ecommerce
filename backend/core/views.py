from rest_framework import viewsets
from .mixins import MultiTenantMixin, AuditoriaMixin

class BaseViewSet(MultiTenantMixin, AuditoriaMixin, viewsets.ModelViewSet):
    pass