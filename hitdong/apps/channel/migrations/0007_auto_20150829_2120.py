# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0006_auto_20150829_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='origin_id',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
