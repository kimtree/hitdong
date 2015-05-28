# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render
from django.template import *

from fedong.apps.video.models import Video
from fedong.apps.crawler.crawler import VideoCrawler, PageCrawler
from fedong.apps.fbpage.models import FbPage


def main(request):
    video_list = Video.objects.extra(select={'score': 'like_count + comment_count'}).all()
    video_list = video_list.extra(order_by=['-score'])

    paginator = Paginator(video_list, 5)

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'videos': videos},
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
