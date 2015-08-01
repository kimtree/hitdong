# -*- coding: utf-8 -*-
import time

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render
from django.template import *
from django.http import HttpResponse

from hitdong.apps.video.models import Video
from hitdong.apps.video.tasks import crawl_videos


def main(request):
    video_list = Video.objects.select_related()
    video_list = video_list.extra(select={'date': 'date(created_at)'})
    video_list = video_list.extra(order_by=['-date', '-metric'])

    paginator = Paginator(video_list, 5)
    total_count = paginator.count

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    for video in videos:
        video.description = video.description.split('\n')[0]

    return render(request, 'index.html',
                  {'videos': videos, 'total_count': total_count},
                  context_instance=RequestContext(request))


def view(request, video_id):
    video = Video.objects.filter(id=video_id).first()
    if video:
        same_page_videos = Video.objects.filter(channel=video.channel)\
                                .exclude(id=video.id)\
                                .order_by('?').all()[:2]

        return render(request, 'video.html',
                      {'video': video, 'same_page_videos': same_page_videos},
                      context_instance=RequestContext(request))
    else:
        return redirect('/')


def crawler(request):
    key = request.GET.get('key', '')

    if key == 'kimtree':
        start_time = time.time()
        crawl_videos.delay()

        return HttpResponse('%s seconds' % (time.time() - start_time))
    else:
        return HttpResponse('Unauthorized', status=401)
