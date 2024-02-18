from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    created_by = models.UUIDField()
    updated_by = models.UUIDField()

class NoteUserMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note_id = models.UUIDField()
    user_id = models.UUIDField()

class NoteVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note_id = models.UUIDField()
    user_id = models.UUIDField()
    description = models.CharField()
    timestamp = models.DateTimeField(default=timezone.now)