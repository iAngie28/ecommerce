from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import connection
from django_tenants.utils import tenant_context
from apps.gestionDeReportes.cu18_gestionar_notificaciones.models.notificacion import Notificacion
from apps.gestionDeReportes.cu18_gestionar_notificaciones.api.serializers import NotificacionSerializer
from apps.gestionDeUsuarioySeguridad.cu1_iniciar_sesion.authentication import ClienteJWTAuthentication, UsuarioJWTAuthentication

class NotificacionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = NotificacionSerializer
    authentication_classes = [ClienteJWTAuthentication, UsuarioJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def _get_user_email(self):
        user = self.request.user
        return getattr(user, 'email', None) or getattr(user, 'correo', None)

    def _get_tenant_host(self, tenant):
        domain = tenant.domains.first()
        return getattr(domain, 'domain', None) or tenant.schema_name

    def _serialize_notification(self, notificacion, tenant=None):
        data = NotificacionSerializer(notificacion).data
        if tenant:
            data['tienda_schema'] = tenant.schema_name
            data['tienda_nombre'] = (
                getattr(tenant, 'nombre_comercial', None)
                or getattr(tenant, 'name', None)
                or tenant.schema_name
            )
            data['tienda_host'] = self._get_tenant_host(tenant)
            data['source_id'] = notificacion.id
        return data

    def _global_cliente_notifications(self, email):
        from apps.customers.models import Client
        from apps.customers.clientes.models.cliente import Cliente

        notifications = []
        for tenant in Client.objects.exclude(schema_name='public'):
            with tenant_context(tenant):
                cliente = Cliente.objects.filter(correo=email).first()
                if not cliente:
                    continue

                queryset = Notificacion.objects.filter(
                    cliente=cliente,
                ).order_by('-fecha_creacion')

                for notificacion in queryset:
                    notifications.append((notificacion.fecha_creacion, self._serialize_notification(notificacion, tenant)))

        notifications.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in notifications]
    
    def get_queryset(self):
        from apps.customers.clientes.models.cliente import Cliente
        
        user = self.request.user
        if not user or not user.is_authenticated:
            return Notificacion.objects.none()
            
        email = getattr(user, 'email', None) or getattr(user, 'correo', None)
        if not email:
            return Notificacion.objects.none()
            
        if connection.schema_name == 'public':
            return Notificacion.objects.none()
            
        try:
            # Intentar buscar como cliente primero
            cliente = Cliente.objects.get(correo=email)
            return Notificacion.objects.filter(cliente=cliente)
        except Cliente.DoesNotExist:
            # Si no es cliente, buscar como usuario (vendedor)
            return Notificacion.objects.filter(usuario=user)

    def list(self, request, *args, **kwargs):
        email = self._get_user_email()
        if connection.schema_name == 'public':
            if not email:
                return Response([], status=status.HTTP_200_OK)
            return Response(self._global_cliente_notifications(email), status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if connection.schema_name != 'public':
            return super().partial_update(request, *args, **kwargs)

        from apps.customers.models import Client
        from apps.customers.clientes.models.cliente import Cliente

        tenant_schema = (
            request.data.get('tenant_schema')
            or request.data.get('tienda_schema')
            or request.query_params.get('tenant_schema')
            or request.query_params.get('tienda_schema')
        )
        email = self._get_user_email()

        if not tenant_schema or not email:
            return Response(
                {'detail': 'tenant_schema es requerido para marcar notificaciones globales.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tenant = Client.objects.filter(schema_name=tenant_schema).first()
        if not tenant:
            return Response({'detail': 'Tienda no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        with tenant_context(tenant):
            cliente = Cliente.objects.filter(correo=email).first()
            if not cliente:
                return Response({'detail': 'Cliente no encontrado en la tienda.'}, status=status.HTTP_404_NOT_FOUND)

            notificacion = Notificacion.objects.filter(
                pk=kwargs.get(self.lookup_url_kwarg or self.lookup_field),
                cliente=cliente,
            ).first()
            if not notificacion:
                return Response({'detail': 'Notificación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(
                notificacion,
                data={'leido': request.data.get('leido', True)},
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(self._serialize_notification(notificacion, tenant))

    @action(detail=False, methods=['post'], url_path='marcar-todas-leidas')
    def marcar_todas_leidas(self, request):
        if connection.schema_name == 'public':
            from apps.customers.models import Client
            from apps.customers.clientes.models.cliente import Cliente

            email = self._get_user_email()
            if not email:
                return Response({'status': 'Sin notificaciones para marcar.'})

            total = 0
            for tenant in Client.objects.exclude(schema_name='public'):
                with tenant_context(tenant):
                    cliente = Cliente.objects.filter(correo=email).first()
                    if not cliente:
                        continue
                    total += Notificacion.objects.filter(
                        cliente=cliente,
                        leido=False,
                    ).update(leido=True)

            return Response({'status': f'{total} notificación(es) marcadas como leídas'})

        queryset = self.get_queryset()
        queryset.filter(leido=False).update(leido=True)
        return Response({'status': 'Todas las notificaciones marcadas como leÃ­das'})

