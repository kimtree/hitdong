# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_video_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagmatch',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='tagmatch',
            name='video',
        ),
        migrations.DeleteModel(
            name='TagMatch',
        ),
    ]
