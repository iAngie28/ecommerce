import uuid
from django.db import models

class VoiceTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, default='PENDING', choices=[
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure')
    ])
    prompt = models.TextField(null=True, blank=True)
    sql_query = models.TextField(null=True, blank=True)
    results = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'voice_task'
        ordering = ['-created_at']

    def __str__(self):
        return f"Task {self.id} - {self.status}"

