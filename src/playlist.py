import os
import isodate
from googleapiclient.discovery import build
from datetime import timedelta


class PlayList:
    """Класс для плейлиста"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.title = self.get_playlist_title()
        self.url = ''.join(['https://www.youtube.com/playlist?list=', self.__playlist_id])

    def get_info(self):
        """По id плейлиста получает данные о элементах плейлиста"""
        playlist = self.get_service().playlistItems().list(part='snippet,contentDetails',
                                                           playlistId=self.__playlist_id
                                                           ).execute()
        return playlist

    def get_playlist_title(self):
        """По id канала получает список плейлистов на канале и из них получает название канала по его id"""
        playlists = self.get_service().playlists().list(channelId=self.get_info()['items'][0]['snippet']['channelId'],
                                                        part='contentDetails,snippet',
                                                        maxResults=50,
                                                        ).execute()

        for playlist in playlists['items']:
            if playlist['id'] == self.__playlist_id:
                return playlist['snippet']['title']

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def get_video_ids(self):
        return [video['contentDetails']['videoId'] for video in self.get_info()['items']]

    @property
    def total_duration(self):

        total_duration = timedelta(hours=0, minutes=0, seconds=0)

        for video_id in self.get_video_ids():
            video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=video_id
                                                     ).execute()
            duration = video['items'][0]['contentDetails']['duration']

            iso_duration = isodate.parse_duration(duration)
            duration_split = str(iso_duration).split(':')
            duration = timedelta(hours=int(duration_split[0]), minutes=int(duration_split[1]),
                                 seconds=int(duration_split[2]))
            total_duration += duration

        return total_duration
