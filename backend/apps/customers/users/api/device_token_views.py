from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.customers.users.models.device_token import DeviceToken
from apps.customers.users.api.device_token_serializer import DeviceTokenSerializer

class DeviceTokenRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeviceTokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            cliente = getattr(request, 'cliente', None)
            usuario = request.user if hasattr(request, 'user') and not cliente else None
            
            if not cliente and not usuario:
                return Response({'error': 'No auth context'}, status=401)
                
            # Buscar si el token ya existe
            device_token, created = DeviceToken.objects.get_or_create(
                token=token,
                defaults={'cliente': cliente, 'usuario': usuario}
            )
            
            # Si existía, asegurarse de que pertenece al usuario actual
            if not created:
                device_token.cliente = cliente
                device_token.usuario = usuario
                device_token.save()

            return Response({'status': 'Token registrado exitosamente'})
        return Response(serializer.errors, status=400)
