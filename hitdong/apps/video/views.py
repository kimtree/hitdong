# -*- coding: utf-8 -*-
import time

import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render
from django.template import *
from django.http import HttpResponse

from hitdong.apps.video.models import Video, Tag
from hitdong.apps.video.tasks import crawl_videos
from hitdong.apps.crawler import VideoCrawler


def main(request):
    video_list = Video.objects.select_related()
    video_list = video_list.filter(is_open=True)
    # video_list = video_list.extra(select={'date': 'date(created_at)'})
    # video_list = video_list.order_by('-date', '-metric', '-created_at')
    video_list = video_list.order_by('-created_at')

    paginator = Paginator(video_list, 10)
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
    video = Video.objects.filter(id=video_id, is_open=True).first()
    if video:
        same_page_videos = Video.objects.filter(channel=video.channel, is_open=True)\
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


def tag(request, tag_id):
    try:
        tag = Tag.objects.get(pk=tag_id)
    except:
        return redirect('/')

    video_list = Video.objects.filter(tags=tag_id, is_open=True).order_by('-created_at')

    paginator = Paginator(video_list, 10)

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'tag.html',
                  {'videos': videos, 'tag': tag},
                  context_instance=RequestContext(request))


@login_required
def manual_adder(request):
    video_id = request.GET.get('video_id')

    if video_id:
        param = {
            'key': settings.YOUTUBE_ACCESS_TOKEN
        }
        param['id'] = video_id

        data = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet',
                            params=param).json()

        item = data['items'][0]
        v = Video(96,  # 힛동 큐레이션 채널로 고정
                  item['id'],
                  item['snippet']['title'],
                  item['snippet']['description'],
                  item['snippet']['thumbnails']['default']['url'],
                  VideoCrawler.convert_tz(item['snippet']['publishedAt']),
                  9999)
        v.save()

        tags = Tag.objects.all()
        for tag in tags:
            if tag.name.lower() in (v.title.lower() or v.description.lower()):
                v.tags.add(tag)

        return redirect('/admin/video/video/' + video_id)

    return render(request, 'manual_adder.html',
                  context_instance=RequestContext(request))
