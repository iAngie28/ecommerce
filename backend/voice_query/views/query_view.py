from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services import VoiceQueryService
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
            prompt = text_query
            if audio_file:
                logger.info(f"Processing audio file: {audio_file.name}")
                prompt = VoiceQueryService.transcribe_audio(audio_file)
            
            if not prompt:
                return Response({"error": "No pude entender lo que dijiste. Intenta de nuevo."}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Prompt understood: {prompt}")
            schema = VoiceQueryService.get_db_schema()
            sql = VoiceQueryService.generate_sql(prompt, schema)
            
            # Si lo que devolvió la IA no parece SQL (no empieza con SELECT o WITH)
            # lo tratamos como una explicación de por qué no pudo generar la consulta.
            upper_sql = sql.upper().strip()
            if not (upper_sql.startswith('SELECT') or upper_sql.startswith('WITH')):
                return Response({
                    "prompt": prompt,
                    "error": sql if sql else "La IA no pudo generar una consulta SQL válida para tu petición."
                }, status=status.HTTP_400_BAD_REQUEST)

            results = VoiceQueryService.execute_query(sql)

            return Response({
                "prompt": prompt,
                "sql": sql,
                "results": results,
                "count": len(results) if results else 0
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Error in VoiceQueryView")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
