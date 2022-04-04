# https://developers.google.com/youtube/v3/docs
# https://github.com/youtube/api-samples/tree/master/python

import json

import pandas as pd
from apiclient.discovery import build

class YouTubeData(object):
    def __init__(self) -> None:
        with open('./data/secret.json') as f:
            secret = json.load(f)

        DEVELOPER_KEY = secret['KEY']
        YOUTUBE_API_SERVICE_NAME = 'youtube'
        YOUTUBE_API_VERSION = 'v3'

        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    def search_video(self, q, max_results=10):
        response = self.youtube.search().list(
            q=q,
            part='id,snippet',
            order='viewCount',
            type='video',
            maxResults=max_results
        ).execute()

        items_id = []
        for item in response['items']:
            item_id = {}
            item_id['video_id'] = item['id']['videoId']
            item_id['channel_id'] = item['snippet']['channelId']
            items_id.append(item_id)

        self.df_video = pd.DataFrame(items_id)

    def extract_video(self, th_subscribers=5000):
        channel_ids = self.df_video['channel_id'].unique().tolist()

        response = self.youtube.channels().list(
            id=','.join(channel_ids),
            part='statistics',
            fields='items(id,statistics(subscriberCount))'
        ).execute()

        items_id = []
        for item in response['items']:
            item_id = {}
            item_id['channel_id'] = item['id']
            try:
                item_id['subscribers'] = int(item['statistics']['subscriberCount'])
            except KeyError:
                item_id['subscribers'] = 0
            items_id.append(item_id)

        df_subscribers = pd.DataFrame(items_id)

        # 動画情報とチャンネル情報の結合
        df = pd.merge(left=self.df_video, right=df_subscribers, on='channel_id')
        self.df_extracted = df[df['subscribers'] < th_subscribers]

    def get_results(self):
        video_ids = self.df_extracted['video_id'].tolist()

        response = self.youtube.videos().list(
            id=','.join(video_ids),
            part='snippet,statistics',
            fields='items(id,snippet(title),statistics(viewCount))'
        ).execute()

        items_id = []
        for item in response['items']:
            item_id = {}
            item_id['video_id'] = item['id']
            item_id['title'] = item['snippet']['title']
            item_id['view_count'] = item['statistics']['viewCount']
            items_id.append(item_id)
        df_video_info = pd.DataFrame(items_id)

        # 動画情報と視聴回数の結合
        self.df_results = pd.merge(left=self.df_extracted, right=df_video_info, on='video_id')

        self.df_results = self.df_results.loc[:, ['video_id', 'title', 'view_count', 'subscribers', 'channel_id']]
        print(self.df_results)


def main():
    q = 'Python 自動化'
    max_results = 50

    youtube_data = YouTubeData()
    youtube_data.search_video(q, max_results)
    youtube_data.extract_video(10000)
    youtube_data.get_results()

if __name__ == '__main__':
    main()