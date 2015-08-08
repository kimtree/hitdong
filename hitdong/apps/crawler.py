import collections
import datetime

import dateutil.parser
import dateutil.tz
import facebook
import requests

Video = collections.namedtuple('Video', 'username, id, title, description, thumbnail, created_at, metric')


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
    BASE_URL = 'https://www.googleapis.com/youtube/v3/'

    def __init__(self, origin_id, access_token):
        ChannelCrawler.__init__(self, 1, origin_id)
        self.access_token = access_token

    def get_profile(self):
        url = self.BASE_URL + 'channels?part=snippet'
        param = {
            'key': self.access_token
        }
        if self.origin_id[:2] == 'UC':
            param['id'] = self.origin_id
        else:
            param['forUsername'] = self.origin_id

        data = requests.get(url, params=param).json()

        if len(data['items']) == 0:
            return None

        return data

    def run(self):
        # Get profile
        data = self.get_profile()
        if data:
            snippet = data['items'][0]['snippet']
            self.name = snippet['localized']['title']
            self.profile_url = snippet['thumbnails']['default']['url']
            self.origin_id = data['items'][0]['id']


class VideoCrawler(object):
    def __init__(self):
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
    def convert_tz(time):
        return dateutil.parser.parse(time).astimezone(dateutil.tz.tzlocal())


class FacebookVideoCrawler(VideoCrawler):
    def __init__(self, username, access_token):
        VideoCrawler.__init__(self)
        self.username = username
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
                    created_at = self.convert_tz(post['created_time'])
                    if self.yesterday <= created_at < self.today:
                        thumbnail_select_idx = int(round(len(post['format']) / 2)) - 1
                        thumbnail = post['format'][thumbnail_select_idx]['picture']
                        comment_count = self.fb.get_connections(post['id'], 'comments', summary=True)['summary']['total_count']
                        like_count = self.fb.get_connections(post['id'], 'likes', summary=True)['summary']['total_count']
                        metric = round((comment_count + like_count))

                        v = Video(self.username,
                                  post['id'],
                                  ' ',
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
    BASE_URL = 'https://www.googleapis.com/youtube/v3/'

    def __init__(self, channel_id, access_token):
        VideoCrawler.__init__(self)
        self.channel_id = channel_id
        self.access_token = access_token

    def get_upload_playlist_id(self):
        playlist_id = None
        url = self.BASE_URL + 'channels?part=contentDetails'
        param = {
            'key': self.access_token
        }
        if self.channel_id[:2] == 'UC':
            param['id'] = self.channel_id
        else:
            param['forUsername'] = self.channel_id

        data = requests.get(url, params=param).json()

        if len(data['items']) > 0:
            contents_detail = data['items'][0]['contentDetails']
            playlist_id = contents_detail['relatedPlaylists']['uploads']

        return playlist_id

    def get_playlist_items(self, playlist_id):
        url = self.BASE_URL + 'playlistItems?part=snippet'
        param = {
            'playlistId': playlist_id,
            'key': self.access_token
        }
        data = requests.get(url, params=param).json()

        return data

    def get_metric(self, video_id):
        url = self.BASE_URL + 'videos?part=statistics'
        param = {
            'key': self.access_token,
            'id': video_id
        }
        data = requests.get(url, params=param).json()

        stat = data['items'][0]['statistics']

        view = int(stat['viewCount'])
        like = int(stat['likeCount'])
        dislike = int(stat['dislikeCount'])
        comments = int(stat['commentCount'])

        metric = int(round((like - dislike) * ((view / 80) + comments)))

        return metric

    def run(self):
        playlist_id = self.get_upload_playlist_id()
        if playlist_id:
            data = self.get_playlist_items(playlist_id)
            for item in data['items']:
                created_at = self.convert_tz(item['snippet']['publishedAt'])
                if self.yesterday <= created_at < self.today:
                    video_id = item['snippet']['resourceId']['videoId']
                    metric = self.get_metric(video_id)

                    v = Video(self.channel_id,
                              video_id,
                              item['snippet']['title'],
                              item['snippet']['description'],
                              item['snippet']['thumbnails']['high']['url'],
                              created_at,
                              metric)
                    self._videos.append(v)
                elif created_at < self.yesterday:
                    break
