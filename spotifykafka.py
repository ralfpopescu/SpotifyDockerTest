from kafka import KafkaConsumer
import os
import json
import requests
import base64
import urllib
from kafka import KafkaProducer

r = requests.get('http://127.0.0.1:5000/access-token')
token = r.text

headers = {"Authorization": "Bearer " + token, }
r = requests.get('https://api.spotify.com/v1/me', headers=headers)
user_data = json.loads(r.text)

USER_ID = user_data.get('id')
spotify_playlist = 'https://api.spotify.com/v1/users/' + USER_ID + '/playlists'

playlist_consumer = KafkaConsumer('playlists', group_id="anystring")
r = requests.get('http://127.0.0.1:5000/playlists')

for msg in playlist_consumer:
    try:
        print(msg)
        value = msg.value.decode('utf-8')
        value = json.loads(value)
        print(value)
        r = requests.post(spotify_playlist, json=value, headers=headers)
        print(r.text)
    except Exception:
        print('ERROR!')
        print(msg)
