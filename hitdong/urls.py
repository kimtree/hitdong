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

    channels = Channel.objects.all()
    for channel in channels:
        if channel.type == 1:
            crawler = YoutubeVideoCrawler(channel.origin_id, settings.YOUTUBE_ACCESS_TOKEN)
            crawler.run()

            for video in crawler.videos:
                if video.id:
                    result = Video.objects.filter(id=video.id).first()
                    if not result:
                        channel = Channel.objects.filter(origin_id=channel.origin_id).first()
                        if channel:
                            description = video.description
                            if channel.id == 2:
                                description = video.description.split('\n')[0]

                            v = Video(channel=channel,
                                      id=video.id,
                                      title=video.title,
                                      description=description,
                                      thumbnail=video.thumbnail,
                                      created_at=video.created_at,
                                      metric=video.metric,
                                      is_open=True)
                            print v


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
