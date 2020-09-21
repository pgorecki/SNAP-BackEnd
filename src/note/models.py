from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import ObjectRoot


class Note(ObjectRoot):
    class Meta:
        db_table = 'note'
        ordering = ['-created_at']

    source_id = models.UUIDField(primary_key=False)
    source_type = models.ForeignKey(ContentType, null=True, related_name='notes', on_delete=models.CASCADE)
    source = GenericForeignKey('source_type', 'source_id')
    title = models.TextField(blank=True, default='')
    text = models.TextField(blank=True, default='')
    effective_date = models.DateTimeField(default=timezone.now)
