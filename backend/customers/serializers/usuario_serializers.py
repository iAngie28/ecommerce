from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializer custom de autenticación.
    Acepta 'username' O 'email' + 'password' para ser compatible con el frontend.
    """
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Unificamos: si viene username, lo usamos como email
        email = attrs.get("email") or attrs.get("username")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email/usuario y contraseña son requeridos.")

        # Autenticamos usando el campo 'email' (USERNAME_FIELD del modelo)
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Credenciales incorrectas.")

        if not user.is_active:
            raise serializers.ValidationError("Este usuario está inactivo.")

        # Generamos los tokens JWT
        refresh = RefreshToken.for_user(user)

        # Añadimos data extra del tenant al payload del JWT
        if user.tenant:
            refresh['schema'] = user.tenant.schema_name
            refresh['tenant_name'] = user.tenant.name

        self.user = user

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class UsuarioCrudSerializer(serializers.ModelSerializer):
    """
    Serializer para el CRUD de usuarios desde el administrador central.
    """
    class Meta:
        from customers.models.usuario import Usuario
        model = Usuario
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'tenant', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user