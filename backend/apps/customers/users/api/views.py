from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings

# Imports de Core y Servicios
from apps.core.views import BaseViewSet
from ..services.usuario_service import UsuarioService
from ..services.auth_service import get_auth_extra_data
from apps.customers.audit.services.bitacora_service import BitacoraService

# Modelos y Serializadores
from apps.customers.users.models.usuario import Usuario
from apps.customers.users.api.serializers import (
    MyTokenObtainPairSerializer, 
    UsuarioCrudSerializer
)
from apps.customers.tenants.api.serializers import TenantCreateSerializer

class MyTokenObtainPairView(APIView):
    """Vista para el inicio de sesiÃ³n con JWT."""
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

        # Registro manual de acceso (Especial para Login)
        BitacoraService.registrar_acceso(request, serializer.user, "LOGIN")

        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Vista para el cierre de sesiÃ³n."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Refresh token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            
            if request.user.is_authenticated:
                BitacoraService.registrar_acceso(request, request.user, "LOGOUT")
            
            token.blacklist()
            return Response({"detail": "SesiÃ³n cerrada correctamente"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Token invÃ¡lido o ya expirado"}, status=status.HTTP_400_BAD_REQUEST)


class UsuarioCrudViewSet(BaseViewSet):
    """
    Vista de usuarios refactorizada. 
    Hereda de BaseViewSet para auditorÃ­a y multi-tenant automÃ¡ticos.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioCrudSerializer
    modulo_auditoria = "Usuario"

    def get_queryset(self):
        from django.db import connection
        qs = super().get_queryset()
        if connection.schema_name != 'public':
            return qs.filter(tenant__schema_name=connection.schema_name)
        return qs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = UsuarioService()

    def perform_create(self, serializer):
        from django.db import connection
        from apps.customers.models import Client
        
        datos = serializer.validated_data.copy()
        
        # AsignaciÃ³n automÃ¡tica de tenant si estamos en una tienda
        if connection.schema_name != 'public' and not datos.get('tenant'):
            tenant = Client.objects.get(schema_name=connection.schema_name)
            datos['tenant'] = tenant
            
        return self.service.crear_usuario(datos)

    def perform_update(self, serializer):
        return self.service.actualizar_usuario(self.get_object(), serializer.validated_data)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        usuario = self.get_object()
        return Response({'id': usuario.id, 'is_active': usuario.is_active})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        usuario = self.get_object()
        self.service.activar(usuario)
        
        # El Mixin detecta el .save() interno del servicio para auditorÃ­a
        return Response({'detail': 'Usuario activado exitosamente', 'is_active': True})

    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        usuario = self.get_object()
        self.service.desactivar(usuario)
        
        return Response({'detail': 'Usuario desactivado exitosamente', 'is_active': False})


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# PERFIL DEL USUARIO AUTENTICADO
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class MiPerfilView(APIView):
    """
    Obtener y actualizar el perfil del usuario autenticado.
    
    GET /api/usuarios/perfil/ â†’ Obtener datos del perfil
    PATCH /api/usuarios/perfil/ â†’ Actualizar datos
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener datos del perfil del usuario autenticado"""
        usuario = request.user
        
        # Si es un cliente (usuario liviano del token)
        if hasattr(usuario, 'role') and usuario.role == "CLIENTE":
            return Response({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'email': usuario.correo,
                'role': usuario.role,
                'is_cliente': True
            }, status=status.HTTP_200_OK)

        # Si es un vendedor/admin (Usuario real del modelo)
        try:
            serializer = UsuarioCrudSerializer(usuario)
            data = serializer.data
            
            # Determinar rol dinÃ¡mico para el frontend (prioridad jerÃ¡rquica)
            if usuario.is_superuser:
                data['role'] = 'admin'
            else:
                # Obtenemos los roles de forma segura para evitar fallos si la migraciÃ³n M2M no se ha aplicado
                try:
                    roles_list = list(usuario.roles.all().order_by('nivel'))
                    if roles_list:
                        rol_principal = roles_list[0]
                        if rol_principal.nivel == 1: data['role'] = 'admin'
                        elif rol_principal.nivel == 2: data['role'] = 'vendedor'
                        else: data['role'] = 'cliente'
                    else:
                        data['role'] = 'vendedor' if usuario.is_staff else 'cliente'
                except Exception:
                    # Fallback si el campo M2M 'roles' no existe todavÃ­a en la DB
                    data['role'] = 'admin' if usuario.is_superuser else ('vendedor' if usuario.is_staff else 'cliente')
            
            # Asegurar que el frontend sepa si es superuser
            data['is_superuser'] = usuario.is_superuser
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            return Response({
                'error': 'Error al procesar el perfil del usuario',
                'detail': str(e),
                'traceback': traceback.format_exc() if settings.DEBUG else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request):
        """Actualizar datos del perfil"""
        usuario = request.user
        serializer = UsuarioCrudSerializer(
            usuario,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TenantCreateView(APIView):
    """CreaciÃ³n de nuevos esquemas (tiendas)."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TenantCreateSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TenantListView(APIView):
    """Listado pÃºblico de tiendas registradas."""
    permission_classes = [AllowAny]

    def get(self, request):
        from apps.customers.models import Client
        from apps.customers.tenants.api.serializers import TiendaPublicSerializer
        tenants = Client.objects.exclude(schema_name='public')
        serializer = TiendaPublicSerializer(tenants, many=True, context={'request': request})
        return Response(serializer.data)


# --- Utilidades y RecuperaciÃ³n de ContraseÃ±a ---

def send_email_ssl(to_email, subject, body):
    from django.core.mail import send_mail
    send_mail(subject, body, settings.EMAIL_HOST_USER, [to_email], fail_silently=False)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email requerido'}, status=400)

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'message': 'Si el email existe, recibirÃ¡s un enlace.'})

        host = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{protocol}://{host}/reset-password/{uid}/{token}/"

        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            return Response({
                'message': 'Email no configurado en el servidor.',
                'dev_reset_url': reset_url
            }, status=503 if not settings.DEBUG else 200)

        try:
            send_email_ssl(
                to_email=email,
                subject='Restablecer contraseÃ±a',
                body=f'Haz clic aquÃ­ para restablecer tu contraseÃ±a:\n\n{reset_url}\n\nEste enlace expira en 24 horas.',
            )
        except Exception as e:
            return Response({'error': f'Error al enviar el email: {str(e)}'}, status=500)

        return Response({'message': 'Si el email existe, recibirÃ¡s un enlace.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not all([uid, token, new_password]):
            return Response({'error': 'Faltan datos'}, status=400)

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = Usuario.objects.get(pk=user_id)
        except (Usuario.DoesNotExist, ValueError):
            return Response({'error': 'Token invÃ¡lido'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Token invÃ¡lido o expirado'}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'ContraseÃ±a actualizada correctamente'})
