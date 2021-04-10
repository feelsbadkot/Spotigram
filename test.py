# Здесь будем просто тестировать разные функции перед их добавлением в spotify_functions.py
# на нем вряд ли будет много коммитов, но все-таки он нам понадобится

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from variables import *
from pprint import pprint

chevelle = 'https://open.spotify.com/artist/56dO9zeHKuU5Gvfc2kxHNw?si=rYVAFv_cQsGWhE4RG9_nAw'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

results = spotify.artist_albums(chevelle, album_type='album', country='RU')
albums = results['items']
pprint(albums)
