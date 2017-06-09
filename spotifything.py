import os
import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib
from kafka import KafkaProducer

app = Flask(__name__)

REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
SPOTIFY_API_URL = "https://api.spotify.com/v1"
# CLIENT_ID = os.environ["CLIENT_ID"]
# CLIENT_SECRET = os.environ["CLIENT_SECRET"]

CLIENT_ID = "0b0b92a99b264a6da92ce78353994034"
CLIENT_SECRET = "fcb8728571c748ecb8e47ac887c96dfc"

kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')

@app.route('/')
def requestAuth():
   return redirect("https://accounts.spotify.com/authorize/?client_id=0b0b92a99b264a6da92ce78353994034&response_type=code&redirect_uri=" + REDIRECT_URI)

@app.route("/redirect")
def requestAccess():
    code = request.args.get('code')
    uri = 'https://accounts.spotify.com/api/token'
    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    code_payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    base64encoded = str(base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode('ascii')), 'ascii')
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)


    response_data = json.loads(post_request.text)

    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    with open('access_token.txt', 'w') as f:
        f.write(access_token)

    return "hi"

@app.route('/access-token')
def get_access_token():
    with open('access_token.txt', 'r') as f:
        return f.read()

@app.route('/playlists')
def create_playlist():
    message = {
        "description": "New playlist description",
        "public": False,
        "name": "New Playlist"
        }
    message = json.dumps(message)
    kafka_producer.send('playlists', message.encode('utf-8'))
    return "hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
