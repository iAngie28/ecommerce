from rest_framework import serializers
from customers.models import Client, Domain, Usuario
from django_tenants.utils import tenant_context
import re


class TenantCreateSerializer(serializers.Serializer):
    # Datos de la tienda
    nombre_tienda = serializers.CharField(max_length=100)
    schema_name   = serializers.SlugField(max_length=50)  # ej: tienda_ropa
    dominio       = serializers.CharField(max_length=100)  # ej: valeria.localhost

    # Datos del dueño
    email         = serializers.EmailField()
    password      = serializers.CharField(write_only=True, min_length=6)
    first_name    = serializers.CharField(max_length=50)
    last_name     = serializers.CharField(max_length=50)

    def validate_schema_name(self, value):
        if Client.objects.filter(schema_name=value).exists():
            raise serializers.ValidationError("Ya existe una tienda con ese schema.")
        if not re.match(r'^[a-z][a-z0-9_]+$', value):
            raise serializers.ValidationError("Solo letras minúsculas, números y guión bajo.")
        return value

    def validate_dominio(self, value):
        if Domain.objects.filter(domain=value).exists():
            raise serializers.ValidationError("Ese dominio ya está en uso.")
        return value

    def validate_email(self, value):
        return value  # el email se valida dentro del tenant_context

    def create(self, validated_data):
        # 1. Crear el tenant
        tenant = Client.objects.create(
            schema_name=validated_data['schema_name'],
            name=validated_data['nombre_tienda'],
        )

        # 2. Crear el dominio
        Domain.objects.create(
            domain=validated_data['dominio'],
            tenant=tenant,
            is_primary=True
        )

        # 3. Crear el usuario admin dentro del contexto del tenant
        with tenant_context(tenant):
            if Usuario.objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError("Ese email ya existe en esta tienda.")

            admin = Usuario.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                is_staff=True,
                is_active=True,
                tenant=tenant,
            )

        return {
            'tienda': tenant.name,
            'schema': tenant.schema_name,
            'dominio': validated_data['dominio'],
            'admin_email': admin.email,
        }