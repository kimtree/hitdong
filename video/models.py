from django.db import models
from fbpage.models import FbPage


class Video(models.Model):
    page = models.ForeignKey(FbPage)
    video_id = models.BigIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
