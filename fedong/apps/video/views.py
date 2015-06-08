# -*- coding: utf-8 -*-
import threading
import Queue

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render
from django.template import *

from fedong.apps.crawler.crawler import VideoCrawler
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
    # 비디오 크롤링
    pages = FbPage.objects.all()

    data_queue = Queue.Queue()
    for page in pages:
        data_queue.put((page.page_id, settings.FACEBOOK_ACCESS_TOKEN))

    # Run Crawler
    for i in range(8):
        t = VideoThread(data_queue)
        t.setDaemon(True)
        t.start()

    data_queue.join()


class VideoThread(threading.Thread):
    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue

    def run(self):
        while True:
            page_id, access_token = self.data_queue.get()

            v = VideoCrawler(page_id, access_token)
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

            self.data_queue.task_done()
