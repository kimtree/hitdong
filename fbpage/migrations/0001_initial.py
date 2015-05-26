# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FbPage',
            fields=[
                ('page_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('icon_url', models.URLField()),
            ],
        ),
    ]
