# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.core.cache import cache
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from hitdong.apps.video import views as video
from hitdong.apps.channel import views as channel


def flush_cache(request):
    cache.clear()
    return redirect('/')


def test(request):
    from hitdong.apps.crawler import FacebookVideoCrawler, YoutubeVideoCrawler
    from hitdong.apps.channel.models import Channel
    from hitdong.apps.video.models import Video, Tag

    crawler = YoutubeVideoCrawler('UCweOkPb1wVVH0Q0Tlj4a5Pw',
                                  settings.YOUTUBE_ACCESS_TOKEN)
    crawler.run()

    for video in crawler.videos:
        if video.id:
            result = Video.objects.filter(id=video.id).first()
            if not result:
                channel = Channel.objects.filter(origin_id='UCweOkPb1wVVH0Q0Tlj4a5Pw').first()
                if channel:
                    if channel.id == 2:
                        description = video.description.split('\n')[0]

                    v = Video(channel=channel,
                              id=video.id,
                              title=video.title,
                              description=description,
                              thumbnail=video.thumbnail,
                              created_at=video.created_at,
                              metric=video.metric)
                    v.save()
                    video = v

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


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', cache_page(60 * 60 * 24)(video.main)),
    url(r'^p/(?P<username>\w+)$', channel.legacy),
    url(r'^c/(?P<id>\w+)$', channel.view),
    url(r'^v/(?P<video_id>\S+)$', video.view),
    url(r'^tag/(?P<tag_id>\S+)$', video.tag),
    url(r'^crawler/channel', channel.crawler),
    url(r'^crawler/video$', video.crawler),
    url(r'^flush$', flush_cache),
    url(r'^test$', test)
]

urlpatterns += [url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})]
