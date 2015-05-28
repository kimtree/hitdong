from django.db import models
from fedong.apps.fbpage.models import FbPage


class Video(models.Model):
    page = models.ForeignKey(FbPage)
    video_id = models.BigIntegerField(unique=True)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(max_length=400)
    like_count = models.IntegerField()
    comment_count = models.IntegerField()
    created_at = models.DateTimeField()

    def __unicode__(self):
        return str(self.video_id)
