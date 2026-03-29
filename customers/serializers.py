from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Obtenemos el token base
        token = super().get_token(user)

        # Añadimos información extra al cuerpo del JWT (Payload)
        if user.tenant:
            token['schema'] = user.tenant.schema_name
            token['tenant_name'] = user.tenant.name
        
        return token

    def validate(self, attrs):
        # Ejecuta la validación estándar (esto genera los tokens access y refresh)
        data = super().validate(attrs)

        # Añadimos datos extra a la respuesta JSON que recibe el Frontend
        if self.user.tenant:
            # Buscamos el dominio asociado a este cliente
            # Usamos .first() para obtener el objeto Domain vinculado
            domain_obj = self.user.tenant.domains.filter(is_primary=True).first()
            
            # Agregamos el subdominio a la respuesta para que React sepa a dónde redirigir
            data['subdomain'] = domain_obj.domain if domain_obj else None
            data['user_name'] = self.user.username
            
        return data