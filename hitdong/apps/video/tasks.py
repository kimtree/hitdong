from celery import task
from celery import group
from django.core.cache import cache
from django.conf import settings
from hitdong.apps.crawler.crawler import FacebookVideoCrawler
from hitdong.apps.fbpage.models import FbPage
from hitdong.apps.video.models import Video


@task
def do_parse(page_id):
    try:
        crawler = FacebookVideoCrawler(page_id, settings.FACEBOOK_ACCESS_TOKEN)
        crawler.run()

        for video in crawler.videos:
            if video.video_id:
                result = Video.objects.filter(video_id=video.video_id).first()
                if not result:
                    page = FbPage.objects.filter(page_id=video.page_id).first()
                    if page:
                        v = Video(page=page, video_id=video.video_id,
                                  description=video.description,
                                  thumbnail=video.thumbnail,
                                  like_count=video.like_count,
                                  comment_count=video.comment_count,
                                  created_at=video.created_at)
                        v.save()
                        cache.clear()
    except:
        print 'error ' + str(page_id)
        pass


@task
def crawl_videos():
    pages = FbPage.objects.all()

    for page in pages:
        do_parse.delay(page.page_id)
