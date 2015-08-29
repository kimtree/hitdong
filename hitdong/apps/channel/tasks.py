from celery import task
from django.conf import settings

from hitdong.apps.channel.models import Channel
from hitdong.apps.crawler import FacebookChannelCrawler, YoutubeChannelCrawler


@task
def do_parse(type, origin_id):
    try:
        if type == 0:
            p = FacebookChannelCrawler(origin_id, settings.FACEBOOK_ACCESS_TOKEN)
        elif type == 1:
            p = YoutubeChannelCrawler(origin_id, settings.YOUTUBE_ACCESS_TOKEN)

        p.run()

        f = Channel.objects.filter(origin_id=origin_id).first()
        if f:
            f.name = p.name
            f.profile_url = p.profile_url
            if type == 1:
                f.origin_id = p.origin_id
            f.save()
    except:
        print 'error ' + origin_id
        pass


@task
def crawl_pages():
    channels = Channel.objects.filter(is_open=True)
    for channel in channels:
        do_parse.delay(channel.type, channel.origin_id)
