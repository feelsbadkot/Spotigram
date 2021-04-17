# Здесь будут находится все функции, возвращающие необходимые нам штуки из Spotify через API сервиса


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import *
from pprint import pprint
from random import choice


ccm = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, 
                               client_secret=SPOTIPY_CLIENT_SECRET)
spoti = spotipy.Spotify(client_credentials_manager=ccm)


def search_for_track(text):
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


def search_for_artist(text):
    s = ' '.join(text.split())
    res = spoti.search(q=s, limit=5, type='artist', market='RU')
    total = []
    if not res['artists']['items']:
        result = '): По вашему запросу ничего не нашлось :('
        total.append(result)
    for i, elem in enumerate(res['artists']['items']):
        index = i + 1
        artist = elem['name']
        link = elem['external_urls']['spotify']
        genres = ', '.join(elem['genres'][:3])
        if elem['images']:
            image = elem['images'][0]['url']
        else:
            image = 'Картинка не нашлась'
        fols= elem['followers']['total']
        if genres:
            result = f'{index}. {artist} ({genres}) - {fols} followers\n{link}'
        else:
            result = f'{index}. {artist} - {fols}\n{link}'
        disc = return_artists_discography(elem['id'])
        top_tracks = return_artist_top_tracks(elem['id'])
        if return_artist_related(elem['id']):
            related = return_artist_related(elem['id'])
        else:
            related = ['']
        total.append({'info': result, 'image': image,
                      'discography': disc,
                      'top_tracks': top_tracks,
                      'related': related})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


def search_for_album(text):
    s = ' '.join(text.split())
    res = spoti.search(q=s, limit=5, type='album', market='RU')
    total = []
    if not res['albums']['items']:
        result = '): По вашему запросу ничего не нашлось :('
        total.append(result)
    for i, elem in enumerate(res['albums']['items']):
        index = i + 1
        artist = elem['artists'][0]['name']
        year = elem['release_date'][:4]
        name = elem['name']
        link = elem['external_urls']['spotify']
        album_type = elem['album_type']
        cover = elem['images'][0]['url']
        result = f'{index}. {artist} - {name} ({year}) [{album_type}]\n{link}'
        total.append({'info': result, 'cover': cover, 'tracks': return_album_tracks(elem['id'])})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


def search_for_playlist(text):
    s = ' '.join(text.split())
    res = spoti.search(q=s, limit=3, type='playlist', market='RU')
    total = []
    if not res['playlists']['items']:
        result = '): По вашему запросу ничего не нашлось :('
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


def return_artist(text):
    res = spoti.search(q=text, type='artist', market='RU')
    items = res['artists']['items']
    if len(items) > 0:
        return items[0]
    return None


def return_artists_discography(data): # дата это словарь, который возвращает функия выше
    res = spoti.artist_albums(data, album_type='album', country='RU')
    albums = res['items'][:]
    total = []
    while res['next']:
        res = spoti.next(res)
        albums.extend(res['items'])
    for i, elem in enumerate(albums[::-1]):
        index = i + 1
        artist = elem['artists'][0]['name']
        year = elem['release_date'][:4]
        name = elem['name']
        link = elem['external_urls']['spotify']
        album_type = elem['album_type']
        cover = elem['images'][0]['url']
        result = f'{index}. {artist} - {name} ({year}) [{album_type}]\n{link}'
        if any(name in i['info'] for i in total):
            continue
        total.append({'info': result, 'cover': cover, 'tracks': return_album_tracks(elem['id'])})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


def return_artist_top_tracks(data):
    res = spoti.artist_top_tracks(data, country='RU')
    top_tracks = res['tracks']
    total = []
    for i, elem in enumerate(top_tracks):
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


def return_artist_related(data):
    res = spoti.artist_related_artists(data)
    related = res['artists'][:3]
    total = []
    for i, elem in enumerate(related):
        index = i + 1
        artist = elem['name']
        link = elem['external_urls']['spotify']
        genres = ', '.join(elem['genres'][:3])
        if elem['images']:
            image = elem['images'][0]['url']
        else:
            image = 'Картинка не нашлась'
        fols= elem['followers']['total']
        if genres:
            result = f'{index}. {artist} ({genres}) - {fols} followers\n{link}'
        else:
            result = f'{index}. {artist} - {fols}\n{link}'
        total.append({'info': result, 'image': image, 
                      'top_tracks': return_artist_top_tracks(elem['id'])})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


def return_album_tracks(data):
    res = spoti.album_tracks(album_id=data, market='RU')
    tracks = res['items'][:]
    total = []
    while res['next']:
        res = spoti.next(res)
        tracks.extend(res['items'])
    for i, elem in enumerate(tracks):
        index = i + 1
        artist = elem['artists'][0]['name']
        name = elem['name']
        minutes = elem["duration_ms"] // 60000
        if minutes < 10:
            minutes = '0' + str(minutes)
        seconds = elem["duration_ms"] % 60000 // 1000
        if seconds < 10:
            seconds = '0' + str(seconds)
        duration = f'{minutes}:{seconds}'
        link = elem['external_urls']['spotify']
        result = f'{index}. {artist} - {name} - {duration}\n{link}'
        total.append(result)
    if len(total) == 1:
        total[0] = total[0][3:]
    return total
        

def return_new_releases():
    res = spoti.new_releases(country='RU', limit=5)
    new = res['albums']['items']
    total = []
    for i, elem in enumerate(new):
        index = i + 1
        artist = elem['artists'][0]['name']
        year = elem['release_date'][:4]
        name = elem['name']
        link = elem['external_urls']['spotify']
        album_type = elem['album_type']
        cover = elem['images'][0]['url']
        result = f'{index}. {artist} - {name} ({year}) [{album_type}]\n{link}'
        if any(name in i['info'] for i in total):
            continue
        total.append({'info': result, 'cover': cover, 'tracks': return_album_tracks(elem['id'])})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total



# pprint(return_new_releases())
# print(*return_artist_related(art), sep='\n')
# chevelle = return_artist('Молчат дома')
# print(*return_artists_discography(chevelle), sep='\n')
# pprint(return_artist('Alexisonfire'))
# print(*search_for_track('suicide season'), sep='\n')
# print(*search_for_album('there is a hell believe me'), sep='\n')
# print(*search_for_playlist('Полный фреш'), sep='\n')