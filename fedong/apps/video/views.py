# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render
from django.template import *

from fedong.apps.crawler.crawler import VideoCrawler, PageCrawler
from fedong.apps.video.models import Video
from fedong.apps.fbpage.models import FbPage

import datetime

import dateutil.tz


def main(request):
    video_list = Video.objects.extra(select={'score': 'like_count + comment_count'}).all()
    video_list = video_list.extra(order_by=['-score'])

    now = datetime.datetime.now(dateutil.tz.tzlocal())
    yesterday = now - datetime.timedelta(days=1)

    min_time = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    max_time = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
    video_list = video_list.filter(created_at__range=(min_time, max_time))

    paginator = Paginator(video_list, 5)
    total_count = paginator.count

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'index.html',
                  {'videos': videos, 'total_count': total_count},
                  context_instance=RequestContext(request))


def view(request, video_id):
    video = Video.objects.filter(video_id=video_id)[0]

    return render(request, 'video.html', {'video': video},
                  context_instance=RequestContext(request))


def crawler(request):
    # 페이지 크롤링 후 프로필 이미지 업데이트
    pages = FbPage.objects.all()
    for page in pages:
        print page
        p = PageCrawler(page.username, settings.FACEBOOK_ACCESS_TOKEN)
        p.run()

        f = FbPage.objects.get(id=page.id)
        if f:
            f.page_id = p.page_id
            f.name = p.name
            f.profile_url = p.profile_url
            f.save()

    # 비디오 크롤링
    pages = FbPage.objects.all()
    for page in pages:
        v = VideoCrawler(page.page_id, settings.FACEBOOK_ACCESS_TOKEN)
        v.run()

        for video in v.videos:
            result = Video.objects.filter(video_id=video.video_id)
            if not result:
                v = Video(page=page, video_id=video.video_id,
                          description=video.description,
                          thumbnail=video.thumbnail,
                          like_count=video.like_count,
                          comment_count=video.comment_count,
                          created_at=video.created_at)
                v.save()
