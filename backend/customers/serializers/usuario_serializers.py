from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Información mínima necesaria en el payload del JWT
        if user.tenant:
            token['schema'] = user.tenant.schema_name
            token['tenant_name'] = user.tenant.name
        return token

    def validate(self, attrs):
        # Aquí solo llamamos a la validación base
        data = super().validate(attrs)
        
        # En lugar de buscar el dominio aquí, 
        # delegaremos la respuesta extendida al Service o a la View.
        # Por ahora, mantenlo limpio.
        return data