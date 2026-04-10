from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from ..serializers.usuario_serializers import MyTokenObtainPairSerializer
from ..services.auth_service import get_auth_extra_data
from customers.models.usuario import Usuario
from customers.serializers.usuario_serializers import UsuarioCrudSerializer
from customers.serializers.tenant_serializer import TenantCreateSerializer


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

        response_data = serializer.validated_data
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


class UsuarioCrudViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioCrudSerializer

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        usuario = self.get_object()
        return Response({'id': usuario.id, 'is_active': usuario.status()})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        usuario = self.get_object()
        usuario.activate()
        return Response({'detail': 'Usuario activado exitosamente', 'is_active': True})

    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        usuario = self.get_object()
        usuario.disable()
        return Response({'detail': 'Usuario desactivado exitosamente', 'is_active': False})


class TenantCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TenantCreateSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TenantListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        from customers.models import Client, Domain
        tenants = Client.objects.exclude(schema_name='public')
        result = []
        for t in tenants:
            domain = Domain.objects.filter(tenant=t).first()
            result.append({
                'nombre': t.name,
                'schema': t.schema_name,
                'dominio': domain.domain if domain else None,
            })
        return Response(result)