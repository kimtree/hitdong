# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.template import *

from .models import Video


def main(request):
    video_list = Video.objects.all()
    paginator = Paginator(video_list, 20)

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'videos': videos},
                  context_instance=RequestContext(request))


def crawler(request):
    import facebook
    import json
    import requests
    import dateutil.parser
    import datetime
    from dateutil.tz import *
    from fbpage.models import FbPage
    from video.models import Video

    now = datetime.datetime.now(tzlocal())
    yesterday = datetime.datetime.now(tzlocal()) - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    APP_ID = '936263079727671'
    APP_SECRET = 'f13c37430e5f2737c7f9362c956b9e34'

    # access_token = facebook.get_app_access_token(APP_ID, APP_SECRET)
    access_token = '936263079727671|RtctC1LG2JGWD3JXmrEcy49qlTI'

    graph = facebook.GraphAPI(access_token)
    page_names = ['moneydoni', 'saesora', 'gagdong']

    for page_name in page_names:
        print page_name
        profile = graph.get_object(page_name)
        try:
            result = FbPage.objects.filter(page_id=profile['id'])
            if not result:
                f = FbPage(page_id=profile['id'], name=profile['name'],
                           icon_url='https://fbstatic-a.akamaihd.net/rsrc.php/v2/yD/r/DggDhA4z4tO.gif')
                f.save()
            else:
                f = result[0]

            posts = graph.get_connections(profile['id'], 'videos')
        except facebook.GraphAPIError as e:
            if e.result['error']['code'] == 190:
                test = graph.extend_access_token(APP_ID, APP_SECRET)
                print test
                '''
                  TODO: ERROR
                '''

        while True:
            try:
                ended = False
                for post in posts['data']:
                    video_url_format = 'https://www.facebook.com/%s/videos/%s/'

                    # UTC to GMT+9
                    created_at = dateutil.parser.parse(post['created_time']).astimezone(tzlocal())
                    if created_at >= yesterday and created_at < today:
                        print post['icon']
                        print video_url_format % (post['from']['id'], post['id'])
                        print post['description']
                        print created_at

                        comments = graph.get_connections(post['id'], 'comments', summary=True)
                        comment_count = comments['summary']['total_count']
                        likes = graph.get_connections(post['id'], 'likes', summary=True)
                        like_count = likes['summary']['total_count']

                        print comment_count, like_count

                        result = Video.objects.filter(video_id=post['id'])
                        if not result:
                            v = Video(page=f, video_id=post['id'],
                                      description=post['description'],
                                      like_count=like_count,
                                      comment_count=comment_count,
                                      created_at=created_at)
                            v.save()

                    elif created_at < yesterday:
                        ended = True

                if ended:
                    break

                # Attempt to make a request to the next page of data, if it exists.
                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                # When there are no more pages (['paging']['next']), break from the
                # loop and end the script.
                break