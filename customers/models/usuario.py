from django.contrib.auth.models import AbstractUser
from django.db import models
from .tenant import Client  # Importación relativa

class Usuario(AbstractUser):
    tenant = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='usuarios',
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'