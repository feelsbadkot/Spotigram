# Здесь будут находится все функции, возвращающие необходимые нам штуки из Spotify через API сервиса


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from config import *
from pprint import pprint
from random import choice

# Менеджер для управления плеером (работает только через код и с заданным никнеймом)
ccm1 = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                    client_secret=SPOTIPY_CLIENT_SECRET,
                    redirect_uri=SPOTIPY_REDIRECT_URI,
                    scope=SCOPE,
                    username='')
# Менеджер для всех остальных запросов
ccm2 = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                client_secret=SPOTIPY_CLIENT_SECRET)

# Клиенты обоих менеджеров
spoti1 = spotipy.Spotify(client_credentials_manager=ccm1)
spoti2 = spotipy.Spotify(client_credentials_manager=ccm2)


# функция поиска трека
def search_for_track(text): 
    s = ' '.join(text.split())
    # формираем запрос на 5 треков для России 
    res = spoti2.search(q=s, limit=5, type='track', market='RU')
    # итоговый список 
    total = [] 
    # если запрос пустой
    if not res['tracks']['items']:
        result = 'По вашему запросу ничего не нашлось :('
        total.append({'info': result, 'uri': ''})
        return total
    # обрабатываем каждый словарь из полученного списка
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
    # убираем номер, если всего один результат
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


# функция поиска исполнителя
def search_for_artist(text):
    s = ' '.join(text.split())
    # формируем запрос на 5 исполнителей для России
    res = spoti2.search(q=s, limit=5, type='artist', market='RU')
    # итоговый список
    total = []
    # если запрос пустой
    if not res['artists']['items']:
        result = '): По вашему запросу ничего не нашлось :('
        total.append({'info': result, 'discography': [],
                      'top_tracks': [], 'related': []})
        return total
    # обрабатываем каждый словарь из полученного списка
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
    # убираем номер, если всего один результат
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


# функция поиска альбома
def search_for_album(text):
    s = ' '.join(text.split())
    # формируем запрос на 5 альбомов для России
    res = spoti2.search(q=s, limit=5, type='album', market='RU')
    # итоговый список
    total = []
    # если результат пустой
    if not res['albums']['items']:
        result = '): По вашему запросу ничего не нашлось :('
        total.append({'info': result, 'tracks': []})
        return total
    # обрабатываем каждый словарь из полученного списка
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
    # убираем номер, если всего один результат
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


# функция поиска плейлиста
def search_for_playlist(text):
    s = ' '.join(text.split())
    # формируем запрос на 3 плейлиста для России
    res = spoti2.search(q=s, limit=3, type='playlist', market='RU')
    # итоговый список
    total = []
    # если результат пустой
    if not res['playlists']['items']:
        result = '): По вашему запросу ничего не нашлось :('
        total.append(result)
        return total
    # обрабатываем каждый словарь из списка
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
    # убираем номер, если всего один результат 
    if len(total) == 1:
        total[0] = total[0][3:]
    return total


# функция, возвращающая словарь с исполнителем
def return_artist(text):
    res = spoti2.search(q=text, type='artist', market='RU')
    items = res['artists']['items']
    if len(items) > 0:
        return items[0]
    return None


# функция для возврата списка с дискографией
def return_artists_discography(data):
    # запрос для всех альбома исполнителя
    res = spoti2.artist_albums(data, album_type='album', country='RU')
    albums = res['items'][:]
    # итоговый список
    total = []
    # берем все альбомы
    while res['next']:
        res = spoti2.next(res)
        albums.extend(res['items'])
    # обрабатываем каждый словарь из списка в хронологическом порядке
    for i, elem in enumerate(albums[::-1]):
        index = i + 1
        artist = elem['artists'][0]['name']
        year = elem['release_date'][:4]
        name = elem['name']
        link = elem['external_urls']['spotify']
        album_type = elem['album_type']
        cover = elem['images'][0]['url']
        result = f'{index}. {artist} - {name} ({year}) [{album_type}]\n{link}'
        # для избежания повторений
        if any(name in i['info'] for i in total): 
            continue
        total.append({'info': result, 'cover': cover, 'tracks': return_album_tracks(elem['id'])})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    # из-за особенностей библиотеки бота приходится ограничиваться только информацией
    return [album['info'] for album in total]


# функция для возврата списка с популярными треками
def return_artist_top_tracks(data):
    # запрос для получения топа треков исполнителя
    res = spoti2.artist_top_tracks(data, country='RU')
    top_tracks = res['tracks'][:5] # берем топ 5
    # итоговый список
    total = []
    # обрабатываем каждый словарь из списка
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
    # из-за особенностей библиотеки бота приходится ограничиваться только информацией 
    return [track['info'] for track in total]


# функция возвращающая похожих исполнителей
def return_artist_related(data):
    # запрос для получения похожих исполнителей
    res = spoti2.artist_related_artists(data)
    # берем трех
    related = res['artists'][:3]
    # итоговый список
    total = []
    # обрабатываем каждый словарь из списка
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
    # если похожие исполнители указаны, то возвращаем какого-то одного
    if total:
        return choice(total)
    # иначе пустой список
    return []


# функция для получения треков с альбома
def return_album_tracks(data):
    # функция для получения трек-листа с альбома
    res = spoti2.album_tracks(album_id=data, market='RU')
    tracks = res['items'][:]
    # итоговый список
    total = []
    # берем все треки
    while res['next']:
        res = spoti2.next(res)
        tracks.extend(res['items'])
    # обрабатываем каждый словарь из списка
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
    # из-за особенностей библиотеки бота приходится ограничиваться только информацией
    return [track['info'] for track in total]


# функция с новинками
def return_new_releases():
    # формируем запрос на 5 новинок для России
    res = spoti2.new_releases(country='RU', limit=5)
    new = res['albums']['items']
    # итоговый список
    total = []
    # обрабатываем каждый словарь из списка
    for i, elem in enumerate(new):
        index = i + 1
        artist = elem['artists'][0]['name']
        year = elem['release_date'][:4]
        name = elem['name']
        link = elem['external_urls']['spotify']
        album_type = elem['album_type']
        cover = elem['images'][0]['url']
        result = f'{index}. {artist} - {name} ({year}) [{album_type}]\n{link}'
        # проверка на повтор
        if any(name in i['info'] for i in total):
            continue
        total.append({'info': result, 'cover': cover, 'tracks': return_album_tracks(elem['id'])})
    if len(total) == 1:
        total[0]['info'] = total[0]['info'][3:]
    return total


# !!!
# Ниже блок с функциями плеера
# Они не реализованы в боте из-за ограниченности библиотеки,
# Но прекрасно работают через код, поэтому я оставил в конце комментарии,
# С их помощью вы в принципе можете попробовать поуправлять своим спотифай плеером
# Для этого в строке 15 в графу username введите id вашего профиля, 
# После запуска вас перебросит на сайт, где вам нужно разрешить спотифаю работать с вашим профилем
# А в терминал ввести ссылку, на которую вас перебросит после 
# !!!


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
# start_playing_track(search_for_track('I don't wanna be me')[0]['uri'])
# pause()
# play()
# next_track()
# previous_track()
# pprint(return_new_releases())
# ton = return_artist('type o negative')['id']
# pprint(return_artists_discography(ton))
# pprint(search_for_track('детка голливуд'))
# pprint(search_for_playlist('хип хоп пушка'))
# pprint(search_for_album('марабу'))
# w = return_artist('Weekend')['id']
# print(return_artists_discography(w))