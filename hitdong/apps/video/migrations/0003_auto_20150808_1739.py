# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_video_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tagmatch',
            old_name='tag_id',
            new_name='tag',
        ),
        migrations.RenameField(
            model_name='tagmatch',
            old_name='video_id',
            new_name='video',
        ),
    ]
