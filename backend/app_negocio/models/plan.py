from django.db import models


class Plan(models.Model):
    """
    Modelo de Plan de Suscripción (SaaS).
    
    Define los límites y precio de cada plan que puede usar un Tenant.
    """
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del Plan'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    precio_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio Mensual'
    )
    precio_anual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio Anual'
    )
    max_usuarios = models.IntegerField(
        verbose_name='Máximo de Usuarios'
    )
    max_productos = models.IntegerField(
        verbose_name='Máximo de Productos'
    )
    facturacion_max = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Límite de Facturación Mensual'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        db_table = 'app_negocio_plan'
        verbose_name = 'Plan de Suscripción'
        verbose_name_plural = 'Planes de Suscripción'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio_mensual}/mes"
