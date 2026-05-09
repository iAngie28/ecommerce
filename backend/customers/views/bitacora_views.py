from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from customers.models.bitacora import Bitacora
from customers.serializers.bitacora_serializer import BitacoraSerializer

class BitacoraListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Bitacora.objects.all()

        modulo      = request.query_params.get('modulo')
        accion      = request.query_params.get('accion')
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')

        if modulo:      queryset = queryset.filter(modulo__icontains=modulo)
        if accion:      queryset = queryset.filter(accion__icontains=accion)
        if fecha_desde: queryset = queryset.filter(fecha__date__gte=fecha_desde)
        if fecha_hasta: queryset = queryset.filter(fecha__date__lte=fecha_hasta)

        serializer = BitacoraSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)