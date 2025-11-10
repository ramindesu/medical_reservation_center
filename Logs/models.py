from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Log(models.Model):

    actor_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    actor_object_id = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')


    action = models.CharField(max_length=255)


    details = models.TextField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} -> {self.action} at {self.timestamp}"

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ['-timestamp']