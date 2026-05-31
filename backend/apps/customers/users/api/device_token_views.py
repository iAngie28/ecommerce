from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.customers.users.models.device_token import DeviceToken
from apps.customers.users.api.device_token_serializer import DeviceTokenSerializer
from apps.customers.users.authentication import ClienteJWTAuthentication, UsuarioJWTAuthentication
from django_tenants.utils import schema_context

class DeviceTokenRegisterView(APIView):
    authentication_classes = [ClienteJWTAuthentication, UsuarioJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeviceTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        token = serializer.validated_data['token']

        # Detectar si es cliente (app móvil) o vendedor (app vendedor)
        auth_payload = getattr(request, 'auth', {})
        role = auth_payload.get('role') if isinstance(auth_payload, dict) else None

        cliente_id = None
        usuario_id = None

        if role == 'CLIENTE':
            cliente_id = auth_payload.get('cliente_id') or auth_payload.get('user_id')
        else:
            # Es vendedor (Usuario)
            usuario_id = request.user.id if request.user and request.user.is_authenticated else None

        if not cliente_id and not usuario_id:
            return Response({'error': 'No se pudo identificar al usuario.'}, status=401)

        # DeviceToken vive en SHARED_APPS -> schema public
        with schema_context('public'):
            from apps.customers.clientes.models.cliente import Cliente
            from apps.customers.users.models.usuario import Usuario

            cliente = Cliente.objects.filter(id=cliente_id).first() if cliente_id else None
            usuario = Usuario.objects.filter(id=usuario_id).first() if usuario_id else None

            device_token, created = DeviceToken.objects.get_or_create(
                token=token,
                defaults={'cliente': cliente, 'usuario': usuario}
            )
            if not created:
                device_token.cliente = cliente
                device_token.usuario = usuario
                device_token.save()

        return Response({'status': 'Token registrado exitosamente'})
