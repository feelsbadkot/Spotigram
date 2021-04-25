# в этом файле лежат переменные для совершения GET-запросов
# их мы получили, зарегистрировав наше приложение на https://developer.spotify.com
import os

TOKEN = str(os.environ.get('token'))
SPOTIPY_CLIENT_ID = str(os.environ.get('client_id')) 
SPOTIPY_CLIENT_SECRET = str(os.environ.get('client_secret')) 
SPOTIPY_REDIRECT_URI = 'https://www.spotify.com/us/account/overview/'
SCOPE = "user-read-playback-state,user-modify-playback-state"

# названия кнопок
SEARCH_TEXT = '🔍Поиск'
HELP_TEXT = '🍼Помощь'
BACK_TEXT = '⬅️Назад'
BACK_TEXT2 = '⬅️Вернуться к опциям'

CALLBACK_SEARCH_TRACK = '🎧Найти трек'
CALLBACK_SEARCH_ARTIST = '🎤Найти исполнителя'
CALLBACK_SEARCH_ALBUM = '🎸Найти альбом'
CALLBACK_SEARCH_PLAYLIST = '⭐️Найти плейлист'
CALLBACK_SEARCH_NOVELTY = '🤡Новинки'