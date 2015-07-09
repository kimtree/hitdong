import time
import threading
import Queue

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import render
from django.template import *
from django.http import HttpResponse

from hitdong.apps.crawler.crawler import PageCrawler
from hitdong.apps.fbpage.models import FbPage
from hitdong.apps.video.models import Video
from hitdong.apps.fbpage.tasks import crawl_pages


def view(request, username):
    fbpage = FbPage.objects.filter(username=username)[0]

    videos = Video.objects.filter(page=fbpage).order_by('-id')

    paginator = Paginator(videos, 10)
    total_count = paginator.count

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'page.html',
                  {'page': fbpage, 'videos': videos},
                  context_instance=RequestContext(request))


def crawler(request):
    key = request.GET.get('key', '')

    if key == 'kimtree':
        start_time = time.time()
        crawl_pages.delay()

        return HttpResponse('%s seconds' % (time.time() - start_time))
    else:
        return HttpResponse('Unauthorized', status=401)
