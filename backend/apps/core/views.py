from django.db import connection
from rest_framework import viewsets, status
from rest_framework.response import Response
from .mixins import AuditoriaMixin

class BaseViewSet(AuditoriaMixin, viewsets.ModelViewSet):
    """
    BaseViewSet que proporciona auditoría automática y manejo de errores con traza.
    """
    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            import traceback
            return Response({
                'error': str(e),
                'traceback': traceback.format_exc(),
                'view': self.__class__.__name__
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        from rest_framework.exceptions import ValidationError
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            print(f"[ValidationError in {self.__class__.__name__}] data={request.data} errors={e.detail}")
            raise