# apps/voice/api/urls.py
from django.urls import path
from .views import VoiceQueryView, VoiceTaskStatusView

urlpatterns = [
    path('vquery/', VoiceQueryView.as_view(), name='voice_query'),
    path('status/<uuid:task_id>/', VoiceTaskStatusView.as_view(), name='voice_task_status'),
]
