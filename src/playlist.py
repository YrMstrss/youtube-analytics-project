import os
from googleapiclient.discovery import build


class PlayList:
    """Класс для плейлиста"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.title = self.get_playlist_title()
        self.url = ''.join(['https://www.youtube.com/playlist?list=', self.__playlist_id])

    def get_chanel_id(self):
        """По id плейлиста получает данные о элементах плейлиста и канале, из которых получает и возвращает id канала"""
        playlist = self.get_service().playlistItems().list(part='snippet,contentDetails',
                                                           playlistId=self.__playlist_id
                                                           ).execute()
        return playlist['items'][0]['snippet']['channelId']

    def get_playlist_title(self):
        """По id канала получает список плейлистов на канале и из них получает название канала по его id"""
        playlists = self.get_service().playlists().list(channelId=self.get_chanel_id(),
                                                        part='contentDetails,snippet',
                                                        maxResults=50,
                                                        ).execute()

        for playlist in playlists['items']:
            if playlist['id'] == self.__playlist_id:
                return playlist['snippet']['title']

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)
