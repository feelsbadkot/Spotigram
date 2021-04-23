from telegram import Bot
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from spotify_functions import search_for_track, search_for_artist, search_for_album, \
    search_for_playlist
import logging
from config import TOKEN
from keyboards import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# названия кнопок
search_text = '🔍Поиск'
help_text = '🍼Помощь'
back_text = '⬅️Назад'
back_text2 = '⬅️Вернуться к опциям'

CALLBACK_SEARCH_TRACK = '🎧Найти трек'
CALLBACK_SEARCH_ARTIST = '🎤Найти исполнителя'
CALLBACK_SEARCH_ALBUM = '🎸Найти альбом'
CALLBACK_SEARCH_PLAYLIST = '⭐️Найти плейлист'


# лог-декоратор
def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка: {e}")
            raise e

    return inner


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Нажмите на клавиатуре поиск(если нет клавиатуры напишите /open)")


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет я SpotiGram')
    update.message.reply_text("Выберете опцию", reply_markup=keyboard1())


def echo(update: Update, context: CallbackContext):
    text = update.message.text
    if text == search_text:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif text == back_text:
        update.message.reply_text("Выберете опцию", reply_markup=keyboard1())
    elif text == back_text2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif text == help_text:
        help(update=update, context=context)
    elif text == CALLBACK_SEARCH_TRACK:
        choice_options(update=update, context=context, option=CALLBACK_SEARCH_TRACK)
    elif text == CALLBACK_SEARCH_ARTIST:
        choice_options(update=update, context=context, option=CALLBACK_SEARCH_ARTIST)
    elif text == CALLBACK_SEARCH_ALBUM:
        choice_options(update=update, context=context, option=CALLBACK_SEARCH_ALBUM)
    elif text == CALLBACK_SEARCH_PLAYLIST:
        choice_options(update=update, context=context, option=CALLBACK_SEARCH_PLAYLIST)

    else:
        update.message.reply_text(f'Я не знаю что ответить на "{update.message.text}"')
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())


def search_track(update: Update, context: CallbackContext):
    if update.message.text == back_text2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif update.message.text == help_text:
        help(update=update, context=context)
    else:
        context.user_data['track'] = update.message.text
        # update.message.reply_text(*search_for_track(context.user_data['track']))
        track_list = search_for_track(context.user_data['track'])
        for song in track_list:
            update.message.reply_text(song['info'])


def search_artist(update: Update, context: CallbackContext):
    if update.message.text == back_text2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif update.message.text == help_text:
        help(update=update, context=context)
    else:
        context.user_data['artist'] = update.message.text
        # update.message.reply_text(*search_for_artist(context.user_data['track']))
        print(*search_for_artist(context.user_data['artist']))


def search_album(update: Update, context: CallbackContext):
    if update.message.text == back_text2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif update.message.text == help_text:
        help(update=update, context=context)
    else:
        context.user_data['album'] = update.message.text
        # update.message.reply_text(*search_for_album(context.user_data['album']))
        print(*search_for_artist(context.user_data['album']))


def search_playlist(update: Update, context: CallbackContext):
    if update.message.text == back_text2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif update.message.text == help_text:
        help(update=update, context=context)
    else:
        context.user_data['playlist'] = update.message.text
        # update.message.reply_text(*search_for_playlist(context.user_data['playlist']))
        playlist_list = search_for_playlist(context.user_data['playlist'])
        for pl in playlist_list:
            update.message.reply_text(pl)


def choice_options(update: Update, context: CallbackContext, option):
    global opt
    if option == CALLBACK_SEARCH_TRACK:
        opt = 1
        update.message.reply_text("Начинаем поиск?", reply_markup=keyboard3())
    if option == CALLBACK_SEARCH_ARTIST:
        opt = 2
        update.message.reply_text("Начинаем поиск?", reply_markup=keyboard3())
    if option == CALLBACK_SEARCH_ALBUM:
        opt = 3
        update.message.reply_text("Начинаем поиск?", reply_markup=keyboard3())
    if option == CALLBACK_SEARCH_PLAYLIST:
        opt = 4
        update.message.reply_text("Начинаем поиск?", reply_markup=keyboard3())


def search(update: Update, context: CallbackContext):
    if opt == 1:
        update.message.reply_text("Введите название трека")
        return opt
    if opt == 2:
        update.message.reply_text("Введите имя исполнителя")
        return opt
    if opt == 3:
        update.message.reply_text("Введите название альбома")
        return opt
    if opt == 4:
        update.message.reply_text("Введите название плейлиста")
        return opt