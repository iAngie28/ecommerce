from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..serializers.usuario_serializers import MyTokenObtainPairSerializer
from ..services.auth_service import get_auth_extra_data


class MyTokenObtainPairView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = MyTokenObtainPairSerializer(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Tokens ya generados por el serializer
        response_data = serializer.validated_data

        # Añadimos info extra del tenant
        extra_data = get_auth_extra_data(serializer.user)
        response_data.update(extra_data)

        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Refresh token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Token inválido o ya expirado"}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from rest_framework.decorators import action
from customers.models.usuario import Usuario
from customers.serializers.usuario_serializers import UsuarioCrudSerializer
from rest_framework.permissions import IsAuthenticated

class UsuarioCrudViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el CRUD de usuarios con endpoints especiales para 
    gestionar el estado de activación (Central Admin).
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioCrudSerializer
    # permission_classes = [IsAuthenticated] # Descomentar para asegurar endpoints
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Retorna si el usuario está activo o desactivado"""
        usuario = self.get_object()
        # Usa el método del modelo recién creado
        return Response({'id': usuario.id, 'is_active': usuario.status()})
        
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activa un usuario"""
        usuario = self.get_object()
        usuario.activate()
        return Response({'detail': 'Usuario activado exitosamente', 'is_active': True})
        
    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        """Desactiva un usuario"""
        usuario = self.get_object()
        usuario.disable()
        return Response({'detail': 'Usuario desactivado exitosamente', 'is_active': False})