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
        pages = FbPage.objects.all()

        data_queue = Queue.Queue()
        output_queue = Queue.Queue()
        for page in pages:
            data_queue.put((page.username, settings.FACEBOOK_ACCESS_TOKEN))

        start_time = time.time()

        # Run Crawler
        for i in range(20):
            t = PageThread(data_queue, output_queue)
            t.setDaemon(True)
            t.start()

        t = DatabaseThread(output_queue)
        t.daemon = True
        t.start()

        data_queue.join()
        output_queue.join()

        return HttpResponse('%s seconds' % (time.time() - start_time))
    else:
        return HttpResponse('Unauthorized', status=401)


class PageThread(threading.Thread):
    def __init__(self, data_queue, output_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.output_queue = output_queue

    def run(self):
        while True:
            username, access_token = self.data_queue.get()

            p = PageCrawler(username, access_token)
            p.run()

            self.output_queue.put(p)

            self.data_queue.task_done()


class DatabaseThread(threading.Thread):
    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue

    def run(self):
        while True:
            p = self.data_queue.get()

            f = FbPage.objects.filter(username=p.username)[0]
            if f:
                f.page_id = p.page_id
                f.name = p.name
                f.profile_url = p.profile_url
                f.likes = p.likes
                f.save()

            self.data_queue.task_done()
