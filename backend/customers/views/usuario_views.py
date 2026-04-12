from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
import ssl
import smtplib
from email.mime.text import MIMEText
from ..serializers.usuario_serializers import MyTokenObtainPairSerializer
from ..services.auth_service import get_auth_extra_data
from ..services.bitacora_service import BitacoraService
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

        # Registro en Bitácora
        BitacoraService.registrar_acceso(request, serializer.user, "LOGIN")

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
            # Registro en Bitácora (antes de invalidar si es posible)
            if request.user.is_authenticated:
                BitacoraService.registrar_acceso(request, request.user, "LOGOUT")
            
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
        
        # Registro en Bitácora
        BitacoraService.registrar_accion(
            request.user, "Usuario", "ACTIVAR", 
            request=request, 
            metadatos={'id_usuario': usuario.id, 'email': usuario.email}
        )
        
        return Response({'detail': 'Usuario activado exitosamente', 'is_active': True})

    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        usuario = self.get_object()
        usuario.disable()
        
        # Registro en Bitácora
        BitacoraService.registrar_accion(
            request.user, "Usuario", "DESACTIVAR", 
            request=request, 
            metadatos={'id_usuario': usuario.id, 'email': usuario.email}
        )
        
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
def send_email_ssl(to_email, subject, body):
    """Envío de email vía Gmail usando SSL directo (puerto 465)"""
    import ssl
    import smtplib
    from email.mime.text import MIMEText
    from django.conf import settings
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, [to_email], msg.as_string())


class PasswordResetRequestView(APIView):
    """Solicita restablecimiento de contraseña generando un token único"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email requerido'}, status=400)

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'message': 'Si el email existe, recibirás un enlace.'})

        # Construir la URL de reset dinámicamente según el entorno (IP o Dominio)
        host = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
        
        # Generar UID y Token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_url = f"{protocol}://{host}/reset-password/{uid}/{token}/"

        try:
            send_email_ssl(
                to_email=email,
                subject='Restablecer contraseña',
                body=f'Haz clic aquí para restablecer tu contraseña:\n\n{reset_url}\n\nEste enlace expira en 24 horas.',
            )
        except Exception as e:
            return Response({'error': f'Error al enviar el email: {str(e)}'}, status=500)

        return Response({'message': 'Si el email existe, recibirás un enlace.'})


class PasswordResetConfirmView(APIView):
    """Confirma el cambio de contraseña validando el token recibido"""
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
            return Response({'error': 'Token inválido'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Token inválido o expirado'}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Contraseña actualizada correctamente'})
