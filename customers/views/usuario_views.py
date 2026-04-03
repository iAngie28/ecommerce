from rest_framework_simplejwt.views import TokenObtainPairView
from ..services.auth_service import get_auth_extra_data

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # 1. Creamos la instancia del serializer con los datos del request
        serializer = self.get_serializer(data=request.data)

        try:
            # 2. Validamos (esto internamente verifica user/password)
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return super().post(request, *args, **kwargs)

        # 3. Obtenemos la respuesta estándar (los tokens access/refresh)
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # 4. CORRECCIÓN: El usuario está en serializer.user después de is_valid()
            user = serializer.user
            
            # 5. Llamamos a tu servicio para la data extra
            extra_data = get_auth_extra_data(user)
            
            # 6. Inyectamos los datos en la respuesta
            response.data.update(extra_data)
            
        return response