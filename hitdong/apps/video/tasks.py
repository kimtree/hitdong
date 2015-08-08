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
                                  metric=video.metric)
                        v.save()

                        video_tagger.delay(v, video.description)
        cache.clear()
    except:
        print 'error ' + str(origin_id)
        pass


@task
def video_tagger(video, description):
    text_to_tag_id = {
        'MV': 2,
        u'여자친구': 5,
        u'에이핑크': 6,
        u'스텔라': 7,
        u'헬로비너스': 8,
        'HelloVenus': 8,
        'Teaser': 9,
        u'멜로디데이': 10,
        'B1A4': 11,
        u'달샤벳': 12
    }

    tags = []
    for k, v in text_to_tag_id.items():
        if k.lower() in description.lower():
            tag = Tag.objects.get(pk=v)
            tags.append(tag)

    for tag in tags:
        video.tags.add(tag)


@task
def crawl_videos():
    channels = Channel.objects.all()
    for channel in channels:
        do_parse.delay(channel.type, channel.origin_id)
