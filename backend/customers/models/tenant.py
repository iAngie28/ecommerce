from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from .plan import Plan

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True
    
    # Relación con Plan de suscripción
    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes',
        verbose_name='Plan de Suscripción'
    )
    
    # Fechas de suscripción
    fecha_inicio_suscripcion = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Inicio de Suscripción'
    )
    
    fecha_fin_suscripcion = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Fin de Suscripción'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )

class Domain(DomainMixin):
    pass