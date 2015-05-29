from django.shortcuts import render
from django.template import *

from fedong.apps.fbpage.models import FbPage
from fedong.apps.video.models import Video


def view(request, username):
    page = FbPage.objects.filter(username=username)[0]

    videos = Video.objects.filter(page=page)

    return render(request, 'page.html', {'page': page, 'videos': videos},
                  context_instance=RequestContext(request))
