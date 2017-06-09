import os
import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib

app = Flask(__name__)

REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
SPOTIFY_API_URL = "https://api.spotify.com/v1"
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

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

   # Auth Step 5: Tokens are Returned to Application
   response_data = json.loads(post_request.text)
   if(len(response_data.items()) is 0):
       return "hi"
   for key,value in response_data.items():
       print (key,value)
   access_token = response_data["access_token"]
   refresh_token = response_data["refresh_token"]
   token_type = response_data["token_type"]
   expires_in = response_data["expires_in"]

   with open('access_token.txt', 'w') as f:
       f.write(access_token)

   return { 'message': 'Success!' }

@app.route('/access-token')
def get_access_token():
   # read access token from file and return to client
   pass

@app.route('/playlists', methods=['POST'])
def create_playlist():
   # produce message to kafka that defines the playlist you want to create
   pass

if __name__ == '__main__':
   app.run(host='0.0.0.0')
