# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.template import *

from .models import Video
from fedong.crawler import FedongCrawler
from fbpage.models import FbPage


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
    page_names = ['moneydoni', 'saesora', 'gagdong']

    for page_name in page_names:
        c = FedongCrawler(page_name)
        c.run()

        result = FbPage.objects.filter(page_id=c.page.id)
        if not result:
            f = FbPage(page_id=c.page.id, name=c.page.name,
                       icon_url=c.icon_url)
            f.save()
        else:
            f = result[0]

        for video in c.videos:
            result = Video.objects.filter(video_id=video.video_id)
            if not result:
                v = Video(page=f, video_id=video.video_id,
                          description=video.description,
                          like_count=video.like_count,
                          comment_count=video.comment_count,
                          created_at=video.created_at)
                v.save()
