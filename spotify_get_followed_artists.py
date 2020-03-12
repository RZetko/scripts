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
#	- run ./spotify_get_followed_artists.py
#	- you will find list of all your followed artists in file ./followed_artists.txt
#	- if you want to get full artist objects with various details like thumbnails, genres etc. return my_artists in function get_artists() instead of final_artists

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

SPOTIPY_CLIENT_ID=''
SPOTIPY_CLIENT_SECRET=''
SPOTIPY_REDIRECT_URI=''
username = ''
scope = 'user-follow-read'

token = util.prompt_for_user_token(
    username=username,
    scope=scope,
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI
)
sp = None

def get_artists():
    ### creates empty list for the artists to be added later
    my_artists = []

    ### gets first 50 artists and adds to the empty my_artists list
    f = sp.current_user_followed_artists(limit=50)['artists']
    my_artists.extend(f['items'])

    ### while there are more items to be obtained ('next' key is true), loops and adds it to the my_artists list
    ### there's supposed to be a function that does this but I couldn't get it to work, should look into it later
    while f['next']:
        f = sp.current_user_followed_artists(
            limit=f['limit'], after=f['cursors']['after'])['artists']
        my_artists.extend(f['items'])
    ### returns a list of all the artists followed by the user
    final_artists = []
	
    for artist in my_artists:
        final_artists.append(artist['name'])

    return final_artists

def save_artists(all_artists):
	with open('followed_artists.txt', 'w', encoding='utf-8') as filehandle:
		for artist in all_artists:
			filehandle.write('%s\n' % artist)

if token:
	sp = spotipy.Spotify(auth=token)
	all_artists = get_artists()
	save_artists(all_artists)
else:
    print("Can't get token for", username)
