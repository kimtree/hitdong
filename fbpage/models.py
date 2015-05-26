from django.db import models


class FbPage(models.Model):
    page_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    icon_url = models.URLField()
