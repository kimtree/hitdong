import time

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render
from django.template import *
from django.http import HttpResponse

from hitdong.apps.channel.models import Channel
from hitdong.apps.video.models import Video
from hitdong.apps.channel.tasks import crawl_pages


def view(request, id):
    try:
        channel = Channel.objects.get(id=id)
    except:
        return redirect('/')

    videos = Video.objects.filter(channel=channel).select_related()
    videos = videos.extra(select={'date': 'date(created_at)'})
    videos = videos.order_by('-date', '-metric', '-created_at')

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


def legacy(request, username):
    channel = Channel.objects.filter(origin_id=username)
    if not channel:
        return redirect('/')
    else:
        channel = channel[0]

    return redirect('/c/' + str(channel.id), permanent=True)


def crawler(request):
    key = request.GET.get('key', '')

    if key == 'kimtree':
        start_time = time.time()
        crawl_pages.delay()

        return HttpResponse('%s seconds' % (time.time() - start_time))
    else:
        return HttpResponse('Unauthorized', status=401)
