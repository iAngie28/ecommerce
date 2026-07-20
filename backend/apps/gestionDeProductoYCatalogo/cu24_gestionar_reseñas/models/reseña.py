from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.gestionDeProductoYCatalogo.cu7_gestionar_productos.models.producto import Producto
from apps.customers.clientes.models.cliente import Cliente

class Reseña(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='reseñas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reseñas')
    calificacion = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True, null=True, max_length=1000)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='APROBADA')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'cu24_gestionar_reseñas'
        db_table = 'app_negocio_resena'
        verbose_name = 'Reseña de Producto'
        verbose_name_plural = 'Reseñas'
        unique_together = ('producto', 'cliente')
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Reseña de {self.cliente.usuario.get_full_name()} para {self.producto.nombre} ({self.calificacion} estrellas)"
