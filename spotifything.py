import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib

app = Flask(__name__)

REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
CLIENT_ID = "0b0b92a99b264a6da92ce78353994034"
CLIENT_SECRET = "fcb8728571c748ecb8e47ac887c96dfc"



@app.route('/')
def requestAuth():
   # r = requests.get("https://accounts.spotify.com/authorize/?client_id=0b0b92a99b264a6da92ce78353994034&response_type=code&redirect_uri=http://127.0.0.1")

   return redirect("https://accounts.spotify.com/authorize/?client_id=0b0b92a99b264a6da92ce78353994034&response_type=code&redirect_uri=" + REDIRECT_URI)

@app.route("/redirect")
def requestAccess():
   code = 'no code'
   code = request.args.get('code')
   uri = 'https://accounts.spotify.com/api/token'
   SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
   code_payload = {
       "grant_type": "authorization_code",
       "code": code,
       "redirect_uri": REDIRECT_URI
   }

   print(str(code_payload))
   print("asdf")

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

   # Auth Step 6: Use the access token to access Spotify API
   authorization_header = {"Authorization":"Bearer {}".format(access_token)}

   # Get profile data
   user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
   profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
   profile_data = json.loads(profile_response.text)

    # Get user playlist data
   playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
   playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
   playlist_data = json.loads(playlists_response.text)

   # Combine profile and playlist data to display
   display_arr = [profile_data] + playlist_data["items"]
   x = playlist_data.keys()
   string = ""
   for y in x:
       string += " " + y


   return string

if __name__ == '__main__':
      app.run(host='0.0.0.0')
