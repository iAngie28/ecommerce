from django.db import models
from apps.customers.clientes.models.cliente import Cliente

class Notificacion(models.Model):
    """
    Modelo para guardar el historial de notificaciones enviadas a los clientes dentro del tenant.
    Permite mostrar las notificaciones In-App (campanita o sección Mis Notificaciones).
    """
    TIPO_CHOICES = [
        ('PAGO', 'Pago'),
        ('PEDIDO', 'Pedido'),
        ('SISTEMA', 'Sistema'),
    ]

    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name='notificaciones',
        verbose_name='Cliente'
    )
    titulo = models.CharField(max_length=200, verbose_name='Título')
    mensaje = models.TextField(verbose_name='Mensaje')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='SISTEMA')
    leido = models.BooleanField(default=False, verbose_name='Leído')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    class Meta:
        db_table = 'app_negocio_notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.titulo} - Cliente: {self.cliente.id} ({'Leído' if self.leido else 'No leído'})"
