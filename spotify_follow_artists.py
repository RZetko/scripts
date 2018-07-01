# Script to automatically follow Spotify artists by their Spotify IDs
#
# Requirements:
#	Python 3
#	spotipy (pip install spotipy)
#
# Usage:
#	- Replace SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
#	with values for your app (you can get these from Spotify API page)
#	- replace username variable with your username
#	- create file artists.txt in same folder as this python script consisting
#	of one artist ID per line in Spotify ID format (ex. 1yDI9pWnlrJmi9kZn3gkCb)
#	- run ./spotify_follow_artists.py

import pprint
import sys
import time

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

SPOTIPY_CLIENT_ID=''
SPOTIPY_CLIENT_SECRET=''
SPOTIPY_REDIRECT_URI=''
username = ''
scope = 'user-follow-modify'
artist_ids = []
artist_ids_sub = []
artist_ids_final = []
artist_counter = 0

file = open("artists.txt", "r",  encoding="utf8") 

for line in file:
    artist_ids.append(line.rstrip())

for artist_id in artist_ids:
    if artist_counter == 49:
        artist_ids_final.append(artist_ids_sub)
        artist_counter = 0
        artist_ids_sub = []
        
    artist_ids_sub.append(artist_id)
    artist_counter += 1

token = util.prompt_for_user_token(
    username=username,
    scope=scope,
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI
)

if token:
    sp = spotipy.Spotify(auth=token)
    # sp.trace = True

    for artist_id_new in artist_ids_final:
        sp.user_follow_artists(artist_id_new)
        time.sleep(10)
else:
    print("Can't get token for", username)

