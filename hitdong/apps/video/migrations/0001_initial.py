# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TagMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_id', models.ForeignKey(to='video.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('thumbnail', models.URLField(max_length=400)),
                ('created_at', models.DateTimeField()),
                ('metric', models.IntegerField()),
                ('is_open', models.BooleanField(default=False)),
                ('channel', models.ForeignKey(to='channel.Channel')),
            ],
        ),
        migrations.AddField(
            model_name='tagmatch',
            name='video_id',
            field=models.ForeignKey(to='video.Video'),
        ),
    ]
