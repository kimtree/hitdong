from django.db import models


class FbPage(models.Model):
    id = models.AutoField(primary_key=True)
    page_id = models.BigIntegerField(null=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    profile_url = models.URLField(max_length=400)

    def __unicode__(self):
        return self.name
