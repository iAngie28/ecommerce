import threading
import tempfile
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from ..services.query_service import VoiceQueryService
from ..models import VoiceTask
import logging

logger = logging.getLogger(__name__)

class VoiceQueryView(APIView):
    def post(self, request):
        logger.info("VoiceQueryView: Received request")
        audio_file = request.FILES.get('audio')
        text_query = request.data.get('text') 

        if not audio_file and not text_query:
            return Response({"error": "No se proporcionó audio ni texto."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a task record
            task = VoiceTask.objects.create(status='PENDING', prompt=text_query)
            
            audio_path = None
            if audio_file:
                # Save audio file to a temporary location to pass to the thread
                with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                    for chunk in audio_file.chunks():
                        tmp.write(chunk)
                    audio_path = tmp.name

            # Spawn background thread
            schema = getattr(connection, 'schema_name', 'public')
            thread = threading.Thread(
                target=VoiceQueryService.run_async_voice_task,
                args=(task.id, schema, text_query, audio_path)
            )
            thread.daemon = True
            thread.start()

            # Return task ID immediately
            return Response({
                "task_id": str(task.id),
                "status": task.status,
                "message": "Tu consulta está siendo procesada."
            }, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            logger.exception("Error en VoiceQueryView al crear tarea")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VoiceTaskStatusView(APIView):
    def get(self, request, task_id):
        try:
            task = VoiceTask.objects.get(id=task_id)
            return Response({
                "task_id": str(task.id),
                "status": task.status,
                "prompt": task.prompt,
                "sql": task.sql_query,
                "results": task.results,
                "error": task.error_message
            }, status=status.HTTP_200_OK)
        except VoiceTask.DoesNotExist:
            return Response({"error": "Tarea no encontrada"}, status=status.HTTP_404_NOT_FOUND)

