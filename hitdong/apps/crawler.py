import collections
import datetime

import dateutil.parser
import dateutil.tz
import facebook
import requests

Video = collections.namedtuple('Video', 'username, id, description, thumbnail, created_at, metric')


class ChannelCrawler(object):
    def __init__(self, type, origin_id):
        self.type = type
        self.name = None
        self.profile_url = None
        self.origin_id = origin_id

    def run(self):
        raise NotImplementedError()


class FacebookChannelCrawler(ChannelCrawler):
    def __init__(self, username, access_token):
        ChannelCrawler.__init__(self, 0, username)
        self.source_name = username

        try:
            self.fb = facebook.GraphAPI(access_token, version='2.3')
        except facebook.GraphAPIError as e:
            if e.result['error']['code'] == 190:
                pass

    def run(self):
        profile = self.fb.get_object(self.source_name)
        profile_img = self.fb.get_connections(profile['id'], 'picture')

        self.name = profile['name']
        self.profile_url = profile_img['url']


class YoutubeChannelCrawler(ChannelCrawler):
    def __init__(self, username, access_token):
        ChannelCrawler.__init__(self, 1, username)
        self.username = username
        self.access_token = access_token

    def get_profile_by_username(self):
        # Get profile
        url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet'
        param = {
            'forUsername': self.username,
            'key': self.access_token
        }
        data = requests.get(url, params=param).json()

        if len(data['items']) == 0:
            return None

        return data

    def run(self):
        # Get profile
        data = self.get_profile_by_username()
        if data:
            self.name = data['items'][0]['snippet']['localized']['title']
            self.profile_url = data['items'][0]['snippet']['thumbnails']['default']['url']


class VideoCrawler(object):
    def __init__(self, username):
        self.username = username
        self._videos = []
        now = datetime.datetime.now(dateutil.tz.tzlocal())
        yesterday = datetime.datetime.now(dateutil.tz.tzlocal()) - datetime.timedelta(days=1)
        yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        self.today = today
        self.yesterday = yesterday

    @property
    def videos(self):
        return self._videos

    def run(self):
        raise NotImplementedError()

    @staticmethod
    def convert_timezone(time):
        return dateutil.parser.parse(time).astimezone(dateutil.tz.tzlocal())


class FacebookVideoCrawler(VideoCrawler):
    def __init__(self, username, access_token):
        VideoCrawler.__init__(self, username)
        try:
            self.fb = facebook.GraphAPI(access_token)
        except facebook.GraphAPIError as e:
            if e.result['error']['code'] == 190:
                pass

    def run(self):
        posts = self.fb.get_connections(self.username, 'videos')

        while True:
            try:
                ended = False
                for post in posts['data']:
                    created_at = self.convert_timezone(post['created_time'])
                    if self.yesterday <= created_at < self.today:
                        thumbnail_select_idx = int(round(len(post['format']) / 2)) - 1
                        thumbnail = post['format'][thumbnail_select_idx]['picture']
                        comment_count = self.fb.get_connections(post['id'], 'comments', summary=True)['summary']['total_count']
                        like_count = self.fb.get_connections(post['id'], 'likes', summary=True)['summary']['total_count']
                        metric = round((comment_count + like_count))

                        v = Video(self.username,
                                  post['id'],
                                  post['description'],
                                  thumbnail,
                                  created_at,
                                  metric)
                        self._videos.append(v)
                    elif created_at < self.yesterday:
                        ended = True

                if ended:
                    break

                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                break


class YoutubeVideoCrawler(VideoCrawler):
    def __init__(self, username, access_token):
        VideoCrawler.__init__(self, username)
        self.access_token = access_token

    def get_channel_id(self):
        channel = YoutubeChannelCrawler(self.username, self.access_token)
        user = channel.get_profile_by_username()

        if len(user['items']) == 0:
            return None

        return user['items'][0]['id']

    def run(self):
        channel_id = self.get_channel_id()
        url = 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails'
        param = {
            'id': channel_id,
            'key': self.access_token
        }
        data = requests.get(url, params=param).json()

        if len(data['items']) > 0:
            playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails%2Cstatus'
            param = {
                'playlistId': playlist_id,
                'key': self.access_token
            }
            data = requests.get(url, params=param).json()

            for item in data['items']:
                created_at = self.convert_timezone(item['snippet']['publishedAt'])

                if self.yesterday <= created_at < self.today:
                    v = Video(self.username,
                          item['contentDetails']['videoId'],
                          item['snippet']['description'],
                          item['snippet']['thumbnails']['high']['url'],
                          created_at,
                          100)
                    self._videos.append(v)
                elif created_at < self.yesterday:
                    break
