# -*- coding: utf-8 -*-
import time
import threading
import Queue

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render
from django.template import *
from django.http import HttpResponse

from hitdong.apps.crawler.crawler import VideoCrawler
from hitdong.apps.video.models import Video
from hitdong.apps.fbpage.models import FbPage

import datetime

import dateutil.tz


def main(request):

    video_list = Video.objects.select_related()
    video_list = video_list.extra(select={'score': '(like_count + comment_count) / likes',
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
    video = Video.objects.filter(video_id=video_id)[0]

    same_page_videos = Video.objects.filter(page=video.page).exclude(video_id=video.video_id).order_by('?').all()[:2]

    return render(request, 'video.html', {'video': video, 'same_page_videos': same_page_videos},
                  context_instance=RequestContext(request))


def crawler(request):
    # 비디오 크롤링
    pages = FbPage.objects.all()

    data_queue = Queue.Queue()
    output_queue = Queue.Queue()
    for page in pages:
        data_queue.put((page, settings.FACEBOOK_ACCESS_TOKEN))

    start_time = time.time()

    # Run Crawler
    for i in range(20):
        t = VideoThread(data_queue, output_queue)
        t.setDaemon(True)
        t.start()

    data_queue.join()

    while not output_queue.empty():
        video = output_queue.get()
        print video.video_id
        result = Video.objects.filter(video_id=video.video_id)
        if not result:
            page = FbPage.objects.filter(page_id=video.page_id)
            if page:
                page = page[0]
            else:
                continue
            v = Video(page=page, video_id=video.video_id,
                      description=video.description,
                      thumbnail=video.thumbnail,
                      like_count=video.like_count,
                      comment_count=video.comment_count,
                      created_at=video.created_at)
            v.save()

    return HttpResponse('%s seconds' % (time.time() - start_time))


class VideoThread(threading.Thread):
    def __init__(self, data_queue, output_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.output_queue = output_queue

    def run(self):
        while True:
            page, access_token = self.data_queue.get()

            v = VideoCrawler(page.page_id, access_token)
            v.run()

            for video in v.videos:
                self.output_queue.put(video)

            self.data_queue.task_done()
