# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20150808_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.CharField(max_length=100, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='is_open',
            field=models.BooleanField(default=False, verbose_name='\uacf5\uac1c'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=200, verbose_name='\ub3d9\uc601\uc0c1 \uc81c\ubaa9'),
        ),
    ]
