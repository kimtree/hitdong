# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_auto_20150808_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.CharField(max_length=100, serialize=False, primary_key=True),
        ),
    ]
