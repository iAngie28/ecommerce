from rest_framework import serializers
from customers.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre', 'correo', 'telefono', 'contrasena',
            'nit', 'fecha_registro', 'activo'
        ]
        read_only_fields = ['id', 'fecha_registro']
    
    def create(self, validated_data):
        """Al crear, encriptar la contraseña."""
        password = validated_data.pop('contrasena', None)
        cliente = Cliente.objects.create(**validated_data)
        if password:
            cliente.set_password(password)
        return cliente
