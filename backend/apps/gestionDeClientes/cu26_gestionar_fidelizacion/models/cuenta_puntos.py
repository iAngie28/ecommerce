from django.db import models
from apps.customers.clientes.models.cliente import Cliente

class CuentaPuntos(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='cuenta_puntos')
    saldo_actual = models.IntegerField(default=0)
    puntos_historicos = models.IntegerField(default=0)  # Total acumulado en su vida
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'cu26_gestionar_fidelizacion'
        db_table = 'app_negocio_cuenta_puntos'
        verbose_name = 'Cuenta de Puntos'
        verbose_name_plural = 'Cuentas de Puntos'

    def __str__(self):
        return f"Cuenta de {self.cliente.usuario.get_full_name()} - Saldo: {self.saldo_actual} pts"
