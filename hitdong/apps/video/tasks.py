from celery import task
from django.conf import settings
from hitdong.apps.crawler.crawler import VideoCrawler
from hitdong.apps.fbpage.models import FbPage
from hitdong.apps.video.models import Video


@task
def do_parse(page_id):
    try:
        video = VideoCrawler(page_id, settings.FACEBOOK_ACCESS_TOKEN)
        video.run()

        if video.video_id:
            result = Video.objects.filter(video_id=video.video_id)
            if not result:
                page = FbPage.objects.filter(page_id=video.page_id)
                if page:
                    page = page[0]
                    v = Video(page=page, video_id=video.video_id,
                              description=video.description,
                              thumbnail=video.thumbnail,
                              like_count=video.like_count,
                              comment_count=video.comment_count,
                              created_at=video.created_at)
                    v.save()
    except:
        pass


@task
def crawl_videos():
    pages = FbPage.objects.all()
    for page in pages:
        do_parse.delay(page.page_id)
