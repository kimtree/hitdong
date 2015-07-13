from celery import task
from django.conf import settings
from hitdong.apps.crawler.crawler import PageCrawler
from hitdong.apps.fbpage.models import FbPage


@task
def do_parse(username):
    try:
        p = PageCrawler(username, settings.FACEBOOK_ACCESS_TOKEN)
        p.run()

        f = FbPage.objects.filter(username=p.username).first()
        if f:
            f.page_id = p.page_id
            f.name = p.name
            f.profile_url = p.profile_url
            f.likes = p.likes
            f.save()
    except:
        print 'error ' + username
        pass


@task
def crawl_pages():
    pages = FbPage.objects.all()
    for page in pages:
        do_parse.delay(page.username)
