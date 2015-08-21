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
                        description = video.description
                        if channel.id == 2:
                            description = description.split('\n')[0]

                        v = Video(channel=channel,
                                  id=video.id,
                                  title=video.title,
                                  description=description,
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
    text_to_tag_id = {
        'MV': 31,
        u'여자친구': 5,
        u'에이핑크': 6,
        u'스텔라': 7,
        u'헬로비너스': 8,
        'HelloVenus': 8,
        'Teaser': 32,
        u'멜로디데이': 10,
        'B1A4': 11,
        u'달샤벳': 12,
        u'미쓰에이': 13,
        u'백아연': 14,
        'AOA': 15,
        u'소녀시대': 16,
        u'아이유': 17,
        u'피에스타': 18,
        u'포미닛': 19,
        u'걸스데이': 22,
        u'레인보우': 23,
        u'나인뮤지스': 24,
        u'스피카': 25,
        u'직캠': 30
    }

    tags = []
    for k, v in text_to_tag_id.items():
        if k.lower() in video.description.lower():
            try:
                tag = Tag.objects.get(pk=v)
                tags.append(tag)
            except:
                pass

    for tag in tags:
        video.tags.add(tag)


@task
def crawl_videos():
    channels = Channel.objects.all()
    for channel in channels:
        do_parse.delay(channel.type, channel.origin_id)
