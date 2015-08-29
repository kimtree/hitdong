# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0003_remove_channel_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='is_open',
            field=models.BooleanField(default=False, verbose_name='\uacf5\uac1c'),
        ),
    ]
