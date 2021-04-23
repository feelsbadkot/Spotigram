# Здесь будут находится все функции, возвращающие необходимые нам штуки из Spotify через API сервиса


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from config import *
from pprint import pprint
from random import choice

ccm1 = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                    client_secret=SPOTIPY_CLIENT_SECRET,
                    redirect_uri=SPOTIPY_REDIRECT_URI,
                    scope=SCOPE,
                    username='s4hwshxdd146amglz9f9y4n30')

ccm2 = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                client_secret=SPOTIPY_CLIENT_SECRET)


spoti1 = spotipy.Spotify(client_credentials_manager=ccm1)
spoti2 = spotipy.Spotify(client_credentials_manager=ccm2)


def search_for_track(text):
    s = ' '.join(text.split())
    res = spoti2.search(q=s, limit=5, type='track', market='RU')
    total = []
    if not res['tracks']['items']:
        result = 'По вашему запросу ничего не нашлось :('
        total.append(result)
        return total
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
        total.append({'info': result, 'uri': elem['uri']})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


def search_for_artist(text):
    s = ' '.join(text.split())
    res = spoti2.search(q=s, limit=5, type='artist', market='RU')
    total = []
    if not res['artists']['items']:
        result = '): По вашему запросу ничего не нашлось :('
        total.append(result)
        return total
    for i, elem in enumerate(res['artists']['items']):
        index = i + 1
        artist = elem['name']
        link = elem['external_urls']['spotify']
        genres = ', '.join(elem['genres'][:3])
        if elem['images']:
            image = elem['images'][0]['url']
        else:
            image = 'Картинка не нашлась'
        fols = elem['followers']['total']
        if genres:
            result = f'{index}. {artist} ({genres}) - {fols} followers\n{link}'
        else:
            result = f'{index}. {artist} - {fols}\n{link}'
        disc = return_artists_discography(elem['id'])
        top_tracks = return_artist_top_tracks(elem['id'])
        if return_artist_related(elem['id']):
            related = return_artist_related(elem['id'])
        else:
            related = []
        total.append({'info': result, 'image': image,
                      'discography': disc,
                      'top_tracks': top_tracks,
                      'related': related})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


def search_for_album(text):
    s = ' '.join(text.split())
    res = spoti2.search(q=s, limit=5, type='album', market='RU')
    total = []
    if not res['albums']['items']:
        result = '): По вашему запросу ничего не нашлось :('
        total.append(result)
        return total
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
    res = spoti2.search(q=s, limit=3, type='playlist', market='RU')
    total = []
    if not res['playlists']['items']:
        result = '): По вашему запросу ничего не нашлось :('
        total.append(result)
        return total
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
    res = spoti2.search(q=text, type='artist', market='RU')
    items = res['artists']['items']
    if len(items) > 0:
        return items[0]
    return None


def return_artists_discography(data):
    res = spoti2.artist_albums(data, album_type='album', country='RU')
    albums = res['items'][:]
    total = []
    while res['next']:
        res = spoti2.next(res)
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
    return [album['info'] for album in total]


def return_artist_top_tracks(data):
    res = spoti2.artist_top_tracks(data, country='RU')
    top_tracks = res['tracks'][:5]
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
        total.append({'info': result, 'uri': elem['uri']})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return [track['info'] for track in total]


def return_artist_related(data):
    res = spoti2.artist_related_artists(data)
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
        fols = elem['followers']['total']
        if genres:
            result = f'{index}. {artist} ({genres}) - {fols} followers\n{link}'
        else:
            result = f'{index}. {artist} - {fols}\n{link}'
        total.append({'info': result, 'image': image,
                      'top_tracks': return_artist_top_tracks(elem['id'])})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    if total:
        return choice(total)
    return []


def return_album_tracks(data):
    res = spoti2.album_tracks(album_id=data, market='RU')
    tracks = res['items'][:]
    total = []
    while res['next']:
        res = spoti2.next(res)
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
        total.append({'info': result, 'uri': elem['uri']})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return [track['info'] for track in total]


def return_new_releases():
    res = spoti2.new_releases(country='RU', limit=5)
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


def play():
    spoti1.start_playback()


def pause():
    spoti1.pause_playback()


def next_track():
    spoti1.next_track()


def previous_track():
    spoti1.previous_track()


def start_playing_track(data):
    try:
        spoti1.start_playback(uris=[data])
    except Exception:
        pass


# start_playing_track(search_for_track('Хаски Реванш')[0]['uri'])
# pprint(return_new_releases())
# chevelle = return_artist('Молчат дома')['id']
# print(*return_artists_discography(chevelle), sep='\n')
# pprint(return_artist('Alexisonfire'))
# print(*search_for_track('Валентина'), sep='\n')
# print(*search_for_album('there is a hell believe me'), sep='\n')
# print(*search_for_playlist('Полный фреш'), sep='\n')
# pprint(search_for_album('опиаты круг'))
# a = return_artist('Kyuss')['id']
# print(return_artist_top_tracks(a))