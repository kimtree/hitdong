import time

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.template import *
from django.http import HttpResponse

from hitdong.apps.channel.models import Channel
from hitdong.apps.video.models import Video
from hitdong.apps.channel.tasks import crawl_pages


def view(request, username):
    channel = Channel.objects.filter(id=username)[0]

    videos = Video.objects.filter(channel=channel).order_by('-id')
    paginator = Paginator(videos, 10)

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'channel.html',
                  {'channel': channel, 'videos': videos},
                  context_instance=RequestContext(request))


def crawler(request):
    key = request.GET.get('key', '')

    if key == 'kimtree':
        start_time = time.time()
        crawl_pages.delay()

        return HttpResponse('%s seconds' % (time.time() - start_time))
    else:
        return HttpResponse('Unauthorized', status=401)
