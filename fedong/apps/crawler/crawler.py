import collections
import datetime

import dateutil.parser
import dateutil.tz
import facebook
import requests

Video = collections.namedtuple('Video', 'video_id, description, thumbnail, like_count, comment_count, created_at')


class PageCrawler(object):
    def __init__(self, username, access_token):
        self.source_name = username
        try:
            self.fb = facebook.GraphAPI(access_token)
        except facebook.GraphAPIError as e:
            if e.result['error']['code'] == 190:
                pass

        self._page_id = None
        self._username = None
        self._name = None
        self._profile_url = None

    @property
    def page_id(self):
        return self._page_id

    @property
    def username(self):
        return self._username

    @property
    def name(self):
        return self._name

    @property
    def profile_url(self):
        return self._profile_url

    def run(self):
        profile = self.fb.get_object(self.source_name)
        profile_img = self.fb.get_connections(profile['id'], 'picture')

        self._page_id = profile['id']
        self._username = profile['username']
        self._name = profile['name']
        self._profile_url = profile_img['url']


class VideoCrawler(object):
    def __init__(self, page_id, access_token):
        self.page_id = page_id
        try:
            self.fb = facebook.GraphAPI(access_token)
        except facebook.GraphAPIError as e:
            if e.result['error']['code'] == 190:
                pass

        self._videos = []

    @property
    def videos(self):
        return self._videos

    def run(self):
        now = datetime.datetime.now(dateutil.tz.tzlocal())
        yesterday = datetime.datetime.now(dateutil.tz.tzlocal()) - datetime.timedelta(days=1)
        yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        posts = self.fb.get_connections(str(self.page_id), 'videos')

        while True:
            try:
                ended = False
                for post in posts['data']:
                    # UTC to GMT+9
                    created_at = dateutil.parser.parse(post['created_time']).astimezone(dateutil.tz.tzlocal())
                    if yesterday <= created_at < today:
                        thumbnail = post['format'][-1]['picture']
                        comments = self.fb.get_connections(post['id'], 'comments', summary=True)
                        comment_count = comments['summary']['total_count']
                        likes = self.fb.get_connections(post['id'], 'likes', summary=True)
                        like_count = likes['summary']['total_count']

                        v = Video(post['id'], post['description'], thumbnail, like_count, comment_count, created_at)
                        self._videos.append(v)
                    elif created_at < yesterday:
                        ended = True

                if ended:
                    break

                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                break
