from django.db import models
from .plan import Plan


class Suscripcion(models.Model):
    """
    Modelo de Suscripción.
    
    Registra el historial de suscripciones de cada Tenant.
    
    Ciclos:
    - MENSUAL: Se renueva cada mes
    - ANUAL: Se renueva cada año
    """
    
    CICLO_CHOICES = [
        ('MENSUAL', 'Mensual'),
        ('ANUAL', 'Anual'),
    ]
    
    tenant = models.ForeignKey(
        'customers.Client',
        on_delete=models.CASCADE,
        related_name='suscripciones',
        verbose_name='Tenant'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.RESTRICT,
        related_name='suscripciones',
        verbose_name='Plan'
    )
    ciclo = models.CharField(
        max_length=20,
        choices=CICLO_CHOICES,
        verbose_name='Ciclo de Facturación'
    )
    fecha_inicio = models.DateField(
        verbose_name='Fecha de Inicio'
    )
    fecha_fin = models.DateField(
        verbose_name='Fecha de Fin'
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Monto'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    fecha_creacion = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        db_table = 'customers_suscripcion'
        verbose_name = 'Suscripción'
        verbose_name_plural = 'Suscripciones'
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.plan.nombre} ({self.ciclo})"
