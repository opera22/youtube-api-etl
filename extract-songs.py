import os
from dotenv import load_dotenv
import json
import time
import requests

'''
NOTE: This step can also be done by using Google Takeout. The Google Takeout method
will return less data (just three columns: URL, title, album title).
'''

load_dotenv()
TEMP_ACCESS_TOKEN = os.getenv('TEMP_ACCESS_TOKEN', None)
PLAYLIST_ITEMS_ENDPOINT = 'https://youtube.googleapis.com/youtube/v3/playlistItems'

params = {
    'playlistId': 'LM',
    'part': 'snippet',
    'maxResults': '50',
    'pageToken': ''
}

headers = {
    'Authorization': f'Bearer {TEMP_ACCESS_TOKEN}'
}

loop_count = 1

while True:
    response_raw = requests.get(PLAYLIST_ITEMS_ENDPOINT, params=params,
                    headers=headers)

    print(f'Grabbing page {loop_count}...')
    response = json.loads(response_raw.content.decode('utf-8'))

    # Do some logic here if needed

    f = open(f'./extract-songs/response{loop_count}.json', 'w')
    f.write(json.dumps(response))
    f.close()

    if 'nextPageToken' not in response:
        break
    else:
        params['pageToken'] = response['nextPageToken']

    loop_count += 1
    # I didn't run into rate-limiting, but this is here just in case.
    time.sleep(0.2)