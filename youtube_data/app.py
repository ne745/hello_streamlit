# https://developers.google.com/youtube/v3/docs
# https://github.com/youtube/api-samples/tree/master/python

import json

import streamlit as st
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
            if item['statistics']:
                item_id['subscribers'] = int(item['statistics']['subscriberCount'])
            else:
                item_id['subscribers'] = 0

            items_id.append(item_id)

        df_subscribers = pd.DataFrame(items_id)

        # 動画情報とチャンネル情報の結合
        df = pd.merge(left=self.df_video, right=df_subscribers, on='channel_id')
        self.df_extracted = df[df['subscribers'] < th_subscribers]

    def fetch_video_info(self):
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

    def get_results(self):
        return self.df_results

    def get_video_ids(self):
        return self.df_results['video_id'].tolist()


def main():
    max_results = 50

    st.title('YouTube分析アプリ')

    st.sidebar.write('## クエリと閾値の設定')
    st.sidebar.write('### クエリの入力')
    query = st.sidebar.text_input('検索クエリを入力してください', '')
    st.sidebar.write('### 閾値の設定')
    threshold = st.sidebar.slider('登録者数の閾値', 1000, 10000, 5000, 1000)

    st.write('### 選択中のパラメータ')
    st.markdown(f"""
    * 検索クエリ: {query}
    * 登録者数の閾値: {threshold}
    """)

    if query:
        # 動画の検索
        youtube_data = YouTubeData()
        youtube_data.search_video(query, max_results)
        youtube_data.extract_video(threshold)
        youtube_data.fetch_video_info()
        results = youtube_data.get_results()

        st.write('### 分析結果', results)

        st.write('### 動画再生')
        video_id = st.selectbox('動画IDを選択してください', youtube_data.get_video_ids())
        video_field = st.empty()
        video_field.write('こちらに動画が表示されます')
        if st.button('ビデオ表示'):
            video_field.video(f'https://youtu.be/{video_id}')


if __name__ == '__main__':
    main()