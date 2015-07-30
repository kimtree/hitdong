# -*- coding: utf-8 -*-
import time
import threading
import Queue

from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import redirect, render
from django.template import *
from django.http import HttpResponse

from hitdong.apps.video.models import Video
from hitdong.apps.fbpage.models import FbPage
from hitdong.apps.video.tasks import crawl_videos

import datetime

import dateutil.tz


def main(request):
    metric = '(like_count + comment_count) / likes'

    video_list = Video.objects.select_related()
    video_list = video_list.extra(select={'score': metric,
                                          'date': 'date(created_at)'})
    video_list = video_list.extra(order_by=['-date', '-score'])

    '''
    now = datetime.datetime.now(dateutil.tz.tzlocal())
    yesterday = now - datetime.timedelta(days=1)

    min_time = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    max_time = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
    video_list = video_list.filter(created_at__range=(min_time, max_time))
    '''

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
    video = Video.objects.filter(video_id=video_id).first()
    if video:

        same_page_videos = Video.objects.filter(page=video.page)\
                                .exclude(video_id=video.video_id)\
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
