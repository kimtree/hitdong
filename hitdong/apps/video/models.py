# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from hitdong.apps.channel.models import Channel


class Video(models.Model):
    channel = models.ForeignKey(Channel)
    id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=200, verbose_name=u'동영상 제목')
    description = models.TextField(blank=True)
    thumbnail = models.URLField(max_length=400)
    created_at = models.DateTimeField(verbose_name=u'등록일')
    metric = models.IntegerField()
    is_open = models.BooleanField(default=False, verbose_name=u'공개')
    tags = models.ManyToManyField('Tag')

    def __unicode__(self):
        if self.title.strip():
            return str(self.id) + ' ' + self.title
        else:
            return str(self.id) + ' ' + self.description.split('\n')[0]

    def get_tag_names(self):
        tag_names = []

        for tag in self.tags.all():
            tag_names.append(tag.name)

        return ', '.join(tag_names)

    get_tag_names.short_description = u'등록된 태그'


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class VideoAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']
    ordering = ['-created_at']
    list_display = ['id', 'created_at', 'title', 'get_tag_names', 'is_open']
