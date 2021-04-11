# Здесь будут находится все функции, возвращающие необходимые нам штуки из Spotify через их API


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import *
from pprint import pprint
import sys


ccm = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, 
                             client_secret=SPOTIPY_CLIENT_SECRET)
spoti = spotipy.Spotify(client_credentials_manager=ccm)


def search_for_track(text: str):
    s = ' '.join(text.split())
    res = spoti.search(q=s, limit=5, type='track', market='RU')
    total = []
    if not res['tracks']['items']:
        result = 'По вашему запросу ничего не нашлось :('
        total.append(result)
    for i, elem in enumerate(res['tracks']['items']):
        index = i + 1
        artist = elem['artists'][0]['name']
        year = elem['album']['release_date'][:4]
        name = elem['name']
        album = elem['album']['name']
        link = elem['external_urls']['spotify']
        if album != name:
            result = f'{index}. {artist} - {name} ({album}, {year})\n{link}'
        else:
            result = f'{index}. {artist} - {name} ({year})\n{link}'
        total.append(result)
    if len(total) == 1:
        total[0] = total[0][3:]
    return total


def search_for_artist(text):
    s = ' '.join(text.split())
    res = spoti.search(q=s, limit=5, type='artist', market='RU')
    total = []
    if not res['artists']['items']:
        result = 'По вашему запросу ничего не нашлось :('
        total.append(result)
    for i, elem in enumerate(res['artists']['items']):
        index = i + 1
        artist = elem['name']
        link = elem['external_urls']['spotify']
        genres = ', '.join(elem['genres'])
        image = elem['images'][0]['url']
        if genres:
            result = f'{index}. {artist} ({genres})\n{link}\n{image}'
        else:
            result = f'{index}. {artist}\n{link}\n{image}'
        total.append(result)
    if len(total) == 1:
        total[0] = total[0][3:]
    return total


def search_for_album(text):
    pass


def search_for_playlist(text):
    pass


# print(*search_for_track('m.,.,/./''),'), sep='\n')
# print(*search_for_artist('01gfgetfeDACFA Ggaeg'), sep='\n')