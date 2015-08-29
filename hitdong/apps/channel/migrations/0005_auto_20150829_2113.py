# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0004_channel_is_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='is_open',
            field=models.BooleanField(default=True, verbose_name='\uacf5\uac1c'),
        ),
    ]
