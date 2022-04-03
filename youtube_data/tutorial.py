import json

from apiclient.discovery import build


with open('./data/secret.json') as f:
    secret = json.load(f)


DEVELOPER_KEY = secret['KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

q = 'Python 自動化'
max_results = 10

# Call the search.list method to retrieve results matching the specified
# query term.
response = youtube.search().list(
    q=q,
    part='id,snippet',
    order='viewCount',
    type='video',
    maxResults=max_results
).execute()

items = response['items']
item = items[0]
print(item)
print(len(item))