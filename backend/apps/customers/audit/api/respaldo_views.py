from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.views import BaseViewSet
from ..models.respaldo import RespaldoSistema
from .respaldo_serializer import RespaldoSerializer
from ..services.respaldo_service import RespaldoService

class RespaldoViewSet(BaseViewSet):
    """
    API para gestiÃ³n de Respaldos con Versionado Encadenado.
    """
    queryset = RespaldoSistema.objects.all()
    serializer_class = RespaldoSerializer
    modulo_auditoria = "Respaldo"

    def get_service(self):
        return RespaldoService()

    def create(self, request, *args, **kwargs):
        """Sobrescribe el POST para ejecutar la creaciÃ³n real del backup"""
        nombre = request.data.get('nombre', 'Respaldo Manual')
        try:
            respaldo = self.get_service().crear_respaldo(nombre)
            serializer = self.get_serializer(respaldo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            return Response({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='historial')
    def historial_encadenado(self, request):
        """Retorna el historial con la lÃ³gica de cola y siguiente"""
        try:
            respaldos = self.get_service().obtener_historial_encadenado()
            serializer = self.get_serializer(respaldos, many=True)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            return Response({
                'error': str(e),
                'traceback': traceback.format_exc(),
                'view': 'RespaldoViewSet.historial_encadenado'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

