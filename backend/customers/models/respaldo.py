from django.db import models
import zlib

class RespaldoSistema(models.Model):
    """
    Guarda snapshots del sistema en formato binario ofuscado.
    Este modelo vive en el esquema público (SHARED_APPS).
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=100)
    blob_data = models.BinaryField(help_text="Datos del respaldo comprimidos y ofuscados")
    checksum = models.CharField(max_length=64, blank=True)
    metadata = models.JSONField(default=dict, help_text="Información técnica del respaldo")

    class Meta:
        verbose_name = "Respaldo del Sistema"
        verbose_name_plural = "Respaldos del Sistema"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Respaldo {self.nombre} - {self.timestamp}"

    @property
    def size_mb(self):
        if self.blob_data:
            return round(len(self.blob_data) / (1024 * 1024), 2)
        return 0
