from django.db import models


class Rol(models.Model):
    """
    Modelo de roles para controlar permisos de usuarios.
    
    Roles predefinidos:
    - ADMIN: Acceso total
    - VENDEDOR: Puede gestionar productos y ver ventas
    - CLIENTE: Acceso limitado (ver su perfil, pedidos)
    - VIEWER: Solo lectura
    """
    
    NIVEL_CHOICES = [
        (1, 'ADMIN'),
        (2, 'VENDEDOR'),
        (3, 'CLIENTE'),
        (4, 'VIEWER'),
    ]
    
    nombre = models.CharField(
        max_length=60,
        unique=True,
        verbose_name='Nombre del Rol'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    nivel = models.IntegerField(
        choices=NIVEL_CHOICES,
        default=4,
        verbose_name='Nivel de Permisos'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        db_table = 'customers_rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nivel']
    
    def __str__(self):
        return self.nombre
