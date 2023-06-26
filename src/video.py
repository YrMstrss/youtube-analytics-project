import os
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-видео"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        self.__video_id = video_id
        try:
            self.title = self.get_info()['items'][0]['snippet']['title']
            self.url = ''.join(['https://www.youtube.com/watch?v=', self.__video_id])
            self.views_counter = self.get_info()['items'][0]['statistics']['viewCount']
            self.like_count = self.get_info()['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url = None
            self.views_counter = None
            self.like_count = None

    def __str__(self):
        return self.title

    def get_info(self):
        video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                 id=self.__video_id
                                                 ).execute()
        return video

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)
