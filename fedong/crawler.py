import collections
import datetime
import json

import dateutil.parser
import dateutil.tz
import facebook
import requests


APP_ID = '936263079727671'
APP_SECRET = 'f13c37430e5f2737c7f9362c956b9e34'

# access_token = facebook.get_app_access_token(APP_ID, APP_SECRET)
ACCESS_TOKEN = '936263079727671|RtctC1LG2JGWD3JXmrEcy49qlTI'

Page = collections.namedtuple('Page', 'id, name, icon_url')
Video = collections.namedtuple('Video', 'video_id, description, like_count, comment_count, created_at')


class FedongCrawler(object):
    def __init__(self, page_name):
        self.page_name = page_name
        try:
            self.fb = facebook.GraphAPI(ACCESS_TOKEN)
        except facebook.GraphAPIError as e:
            if e.result['error']['code'] == 190:
                test = graph.extend_access_token(APP_ID, APP_SECRET)
                print test
                '''
                  TODO: ERROR
                '''

        self._page = None
        self._videos = []
        self._icon_url = ''

    def run(self):
        self._get_page_info()
        self._get_videos()

    @property
    def page(self):
        return self._page

    @property
    def videos(self):
        return self._videos

    @property
    def icon_url(self):
        return self._icon_url

    def _get_page_info(self):
        profile = self.fb.get_object(self.page_name)
        print profile['name']
        self._page = Page(profile['id'], profile['name'], '')

    def _get_videos(self):
        now = datetime.datetime.now(dateutil.tz.tzlocal())
        yesterday = datetime.datetime.now(dateutil.tz.tzlocal()) - datetime.timedelta(days=1)
        yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        posts = self.fb.get_connections(self._page.id, 'videos')

        while True:
            try:
                ended = False
                for post in posts['data']:
                    # UTC to GMT+9
                    created_at = dateutil.parser.parse(post['created_time']).astimezone(dateutil.tz.tzlocal())
                    if created_at >= yesterday and created_at < today:
                        comments = self.fb.get_connections(post['id'], 'comments', summary=True)
                        comment_count = comments['summary']['total_count']
                        likes = self.fb.get_connections(post['id'], 'likes', summary=True)
                        like_count = likes['summary']['total_count']

                        self._icon_url = post['icon']

                        v = Video(post['id'], post['description'], like_count, comment_count, created_at)
                        self._videos.append(v)
                    elif created_at < yesterday:
                        ended = True

                if ended:
                    break

                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                break
