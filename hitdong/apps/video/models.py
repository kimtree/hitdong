from django.db import models
from hitdong.apps.channel.models import Channel


class Video(models.Model):
    channel = models.ForeignKey(Channel)
    id = models.CharField(primary_key=True, max_length=100, unique=True)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(max_length=400)
    created_at = models.DateTimeField()
    metric = models.IntegerField()

    def __unicode__(self):
        return str(self.id)
