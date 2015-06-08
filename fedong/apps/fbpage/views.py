import threading
import Queue

from django.conf import settings
from django.shortcuts import render
from django.template import *

from fedong.apps.crawler.crawler import PageCrawler
from fedong.apps.fbpage.models import FbPage
from fedong.apps.video.models import Video


def view(request, username):
    page = FbPage.objects.filter(username=username)[0]

    videos = Video.objects.filter(page=page)

    return render(request, 'page.html', {'page': page, 'videos': videos},
                  context_instance=RequestContext(request))


def crawler(request):
    pages = FbPage.objects.all()

    data_queue = Queue.Queue()
    for page in pages:
        data_queue.put((page.username, settings.FACEBOOK_ACCESS_TOKEN))

    # Run Crawler
    for i in range(4):
        t = PageThread(data_queue)
        t.setDaemon(True)
        t.start()

    data_queue.join()


class PageThread(threading.Thread):
    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue

    def run(self):
        while True:
            username, access_token = self.data_queue.get()

            p = PageCrawler(username, access_token)
            p.run()

            f = FbPage.objects.filter(username=username)[0]
            if f:
                print p.page_id, p.name
                f.page_id = p.page_id
                f.name = p.name
                f.profile_url = p.profile_url
                f.likes = p.likes
                f.save()

            self.data_queue.task_done()