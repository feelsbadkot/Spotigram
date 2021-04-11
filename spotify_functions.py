# Здесь будут находится все функции, возвращающие необходимые нам штуки из Spotify через их API


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import *
# from pprint import pprint


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
        minutes = elem["duration_ms"] // 60000
        if minutes < 10:
            minutes = '0' + str(minutes)
        seconds = elem["duration_ms"] % 60000 // 1000
        if seconds < 10:
            seconds = '0' + str(seconds)
        duration = f'{minutes}:{seconds}'
        link = elem['external_urls']['spotify']
        if album != name:
            result = f'{index}. {artist} - {name} ({album}, {year}) - {duration}\n{link}'
        else:
            result = f'{index}. {artist} - {name} ({year}) - {duration}\n{link}'
        total.append(result)
    if len(total) == 1:
        total[0] = total[0][3:]
    return total


def search_for_artist(text: str):
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


def search_for_album(text: str):
    s = ' '.join(text.split())
    res = spoti.search(q=s, limit=5, type='album', market='RU')
    total = []
    if not res['albums']['items']:
        result = 'По вашему запросу ничего не нашлось :('
        total.append(result)
    for i, elem in enumerate(res['albums']['items']):
        index = i + 1
        artist = elem['artists'][0]['name']
        year = elem['release_date'][:4]
        name = elem['name']
        link = elem['external_urls']['spotify']
        album_type = elem['album_type']
        # genres = ', '.join(elem['genres'])
        cover = elem['images'][0]['url']
        # copyrights = elem['copyrights'][0]['text']
        result = f'{index}. {artist} - {name} ({year}) ' + \
                 f'[{album_type}]\n{link}\n{cover}\n'
        total.append(result)
    if len(total) == 1:
        total[0] = total[0][3:]
    return total


def search_for_playlist(text: str):
    s = ' '.join(text.split())
    res = spoti.search(q=s, limit=3, type='playlist', market='RU')
    total = []
    if not res['playlists']['items']:
        result = 'По вашему запросу ничего не нашлось :('
        total.append(result)
    for i, elem in enumerate(res['playlists']['items']):
        index = i + 1
        link = elem['external_urls']['spotify']
        name = elem['name']
        length = elem['tracks']['total']
        owner = elem['owner']['id']
        if length != 1:
            result = f'{index}. "{name}" by {owner} ({length} tracks)\n{link}'
        else:
            result = f'{index}. "{name}" by {owner} ({length} track)\n{link}'
        total.append(result)
    if len(total) == 1:
        total[0] = total[0][3:]
    return total


# print(*search_for_track('suicide season'), sep='\n')
# print(*search_for_album('there is a hell believe me'), sep='\n')
# print(*search_for_artist('01gfgetfeDACFA Ggaeg'), sep='\n')
# print(*search_for_playlist('Полный фреш'), sep='\n')