# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_auto_20150808_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(to='video.Tag'),
        ),
    ]
