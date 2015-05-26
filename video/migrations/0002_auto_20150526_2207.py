# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_squashed_0003_auto_20150526_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='page',
            field=models.ForeignKey(to='fbpage.FbPage'),
        ),
    ]
