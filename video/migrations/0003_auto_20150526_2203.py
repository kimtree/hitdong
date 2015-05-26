# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fbpage', '0001_initial'),
        ('video', '0002_auto_20150526_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='page_id',
        ),
        migrations.AddField(
            model_name='video',
            name='page',
            field=models.ForeignKey(default=datetime.datetime(2015, 5, 26, 13, 3, 53, 477752, tzinfo=utc), to='fbpage.FbPage'),
            preserve_default=False,
        ),
    ]
