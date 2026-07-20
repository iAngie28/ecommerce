from django.db import models
from .cuenta_puntos import CuentaPuntos

class HistorialPuntos(models.Model):
    TIPO_OPERACION = (
        ('ACUMULACION', 'Acumulación por Compra'),
        ('CANJE', 'Canje por Descuento'),
        ('AJUSTE', 'Ajuste Manual'),
    )

    cuenta = models.ForeignKey(CuentaPuntos, on_delete=models.CASCADE, related_name='historial')
    tipo_operacion = models.CharField(max_length=20, choices=TIPO_OPERACION)
    monto_puntos = models.IntegerField()  # Positivo si es ACUMULACION, negativo si es CANJE
    referencia = models.CharField(max_length=100, blank=True, null=True) # Ej. "Pedido #1023"
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'cu26_gestionar_fidelizacion'
        db_table = 'app_negocio_historial_puntos'
        verbose_name = 'Historial de Puntos'
        verbose_name_plural = 'Historial de Puntos'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo_operacion} de {self.monto_puntos} pts en {self.cuenta.cliente.usuario.username}"
