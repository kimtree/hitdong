# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.IntegerField(choices=[(0, b'Facebook'), (1, b'Youtube')])),
                ('name', models.CharField(max_length=100)),
                ('profile_url', models.URLField(max_length=400)),
                ('origin_id', models.CharField(max_length=200)),
            ],
        ),
    ]
