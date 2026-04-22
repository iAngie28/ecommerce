from django.db import models
from django.contrib.auth.hashers import make_password


class Cliente(models.Model):
    """
    Modelo de Cliente (Customer público).
    
    Diferencia con Usuario:
    - Usuario = Admin/empleado de la tienda (tiene tenant_id)
    - Cliente = Customer que compra (NO tiene tenant_id, es público)
    
    Un Cliente puede comprar en múltiples tiendas.
    """
    
    nombre = models.CharField(
        max_length=150,
        verbose_name='Nombre Completo'
    )
    correo = models.EmailField(
        unique=True,
        verbose_name='Correo Electrónico'
    )
    telefono = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    contrasena = models.CharField(
        max_length=255,
        verbose_name='Contraseña'
    )
    nit = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name='NIT (Número de Identificación Tributaria)'
    )
    fecha_registro = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        db_table = 'customers_cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombre} ({self.correo})"
    
    def set_password(self, raw_password):
        """Encripta la contraseña antes de guardar"""
        self.contrasena = make_password(raw_password)
        self.save(update_fields=['contrasena'])
    
    def check_password(self, raw_password):
        """Verifica si la contraseña es correcta"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.contrasena)
