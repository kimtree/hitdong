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
    pass

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
    url(r'^video/add$', video.manual_adder),
    url(r'^test$', test)
]

urlpatterns += [url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})]
