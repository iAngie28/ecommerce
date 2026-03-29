from django.contrib.auth.models import AbstractUser
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

# 1. Tu modelo de Cliente (se queda en SHARED_APPS)
class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

class Domain(DomainMixin):
    pass

# 2. Tu nuevo modelo de Usuario Global
class Usuario(AbstractUser):
    # Relacionamos al usuario con un cliente específico
    tenant = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='usuarios',
        null=True, # Null para superusuarios globales si lo deseas
        blank=True
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'