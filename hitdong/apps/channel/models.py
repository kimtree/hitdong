from django.db import models


class Channel(models.Model):
    TYPES = (
        (0, 'Facebook'),
        (1, 'Youtube')
    )

    id = models.AutoField(primary_key=True)
    type = models.IntegerField(choices=TYPES)
    name = models.CharField(max_length=100)
    profile_url = models.URLField(max_length=400)
    origin_id = models.CharField(max_length=200)

    def __unicode__(self):
        return self._get_type_name(self.type) + ' ' + self.name

    def _get_type_name(self, type):
        return self.TYPES[type][1]
