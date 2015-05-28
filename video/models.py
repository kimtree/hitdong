from django.db import models
from fbpage.models import FbPage


class Video(models.Model):
    page = models.ForeignKey(FbPage)
    video_id = models.BigIntegerField()
    description = models.TextField(blank=True)
    like_count = models.IntegerField()
    comment_count = models.IntegerField()
    created_at = models.DateTimeField()

    def __unicode__(self):
        return str(self.video_id)
