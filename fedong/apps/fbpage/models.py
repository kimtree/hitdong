from django.db import models


class FbPage(models.Model):
    id = models.AutoField(primary_key=True)
    page_id = models.BigIntegerField(null=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    profile_url = models.URLField(max_length=400)

    def __unicode__(self):
        return self.name
