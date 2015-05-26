# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    replaces = [(b'video', '0001_initial'), (b'video', '0002_auto_20150526_2126'), (b'video', '0003_auto_20150526_2203')]

    dependencies = [
        ('fbpage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_id', models.BigIntegerField()),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('page', models.ForeignKey(default=datetime.datetime(2015, 5, 26, 13, 3, 53, 477752, tzinfo=utc), to='fbpage.FbPage')),
            ],
        ),
    ]
