# -*- coding: utf-8 -*-
from celery import task
from django.core.cache import cache
from django.conf import settings

from hitdong.apps.crawler import FacebookVideoCrawler, YoutubeVideoCrawler
from hitdong.apps.channel.models import Channel
from hitdong.apps.video.models import Video, Tag


@task
def do_parse(type, origin_id):
    try:
        if type == 0:
            crawler = FacebookVideoCrawler(origin_id, settings.FACEBOOK_ACCESS_TOKEN)
        elif type == 1:
            crawler = YoutubeVideoCrawler(origin_id, settings.YOUTUBE_ACCESS_TOKEN)

        crawler.run()

        for video in crawler.videos:
            if video.id:
                result = Video.objects.filter(id=video.id).first()
                if not result:
                    channel = Channel.objects.filter(origin_id=origin_id).first()
                    if channel:
                        v = Video(channel=channel,
                                  id=video.id,
                                  title=video.title,
                                  description=video.description,
                                  thumbnail=video.thumbnail,
                                  created_at=video.created_at,
                                  metric=video.metric,
                                  is_open=True)
                        v.save()

                        video_tagger.delay(v)
        cache.clear()
    except:
        print 'error ' + str(origin_id)
        pass


@task
def video_tagger(video):
    tags = Tag.objects.all()
    for tag in tags:
        if tag.name.lower() in (video.title.lower() or video.description.lower()):
            video.tags.add(tag)


@task
def crawl_videos():
    channels = Channel.objects.filter(is_open=True)
    for channel in channels:
        do_parse.delay(channel.type, channel.origin_id)
