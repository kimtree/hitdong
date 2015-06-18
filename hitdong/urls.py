"""fedong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from hitdong.apps.fbpage import views as page
from hitdong.apps.video import views as video


def flush_cache(request):
    cache.clear()
    return redirect('/')


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', cache_page(60 * 60 * 24)(video.main)),
    url(r'^p/(?P<username>\w+)$', page.view),
    url(r'^v/(?P<video_id>[0-9]+)$', video.view),
    url(r'^crawler/page$', page.crawler),
    url(r'^crawler/video$', video.crawler),
    url(r'^flush$', flush_cache)
]

urlpatterns += [url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})]
