# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0002_channel_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='tags',
        ),
    ]
