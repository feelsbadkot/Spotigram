from telegram import Bot
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove
from spotify_functions import search_for_track, search_for_artist, search_for_album, \
    search_for_playlist
import logging
from config import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

search_text = '🔍Поиск'
help_text = '🍼Помощь'
back_text = '⬅️Назад'
# словарь с названиями кнопок
CALLBACK_SEARCH_TRACK = '🎧Найти трек'
CALLBACK_SEARCH_ARTIST = '🎤Найти исполнителя'
CALLBACK_SEARCH_ALBUM = '🎸Найти альбом'
CALLBACK_SEARCH_PLAYLIST = '⭐️Найти плейлист'


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
    keyboard1(update=update, context=context)


def echo(update: Update, context: CallbackContext):
    text = update.message.text
    if text == search_text:
        keyboard2(update=update, context=context)
    elif text == back_text:
        keyboard1(update=update, context=context)
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
        keyboard2(update=update, context=context)


def search_track(update: Update, context: CallbackContext):
    context.user_data['track'] = update.message.text
    #update.message.reply_text(*search_for_track(context.user_data['track']))
    print(*search_for_track(context.user_data['track']))


def search_artist(update: Update, context: CallbackContext):
    context.user_data['artist'] = update.message.text
    # update.message.reply_text(*search_for_artist(context.user_data['track']))
    print(*search_for_artist(context.user_data['artist']))


def search_album(update: Update, context: CallbackContext):
    context.user_data['album'] = update.message.text
    # update.message.reply_text(*search_for_album(context.user_data['album']))
    print(*search_for_artist(context.user_data['album']))


def search_playlist(update: Update, context: CallbackContext):
    context.user_data['playlist'] = update.message.text
    # update.message.reply_text(*search_for_playlist(context.user_data['playlist']))
    print(*search_for_artist(context.user_data['playlist']))


def keyboard1(update: Update, context: CallbackContext):
    reply_keyboard = [[KeyboardButton(text=search_text), KeyboardButton(text=help_text)]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                       one_time_keyboard=False)
    update.message.reply_text(
        "Выберете опцию",
        reply_markup=reply_markup
    )


def close_keyboard(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Клавиатура свернута",
        reply_markup=ReplyKeyboardRemove()
    )


def keyboard2(update: Update, context: CallbackContext):
    keyboard = [
        [
            KeyboardButton(CALLBACK_SEARCH_TRACK),
            KeyboardButton(CALLBACK_SEARCH_ARTIST)
        ],
        [
            KeyboardButton(CALLBACK_SEARCH_ALBUM),
            KeyboardButton(CALLBACK_SEARCH_PLAYLIST)
        ],
        [
            KeyboardButton(back_text),
            KeyboardButton(help_text)
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
                                       one_time_keyboard=False)
    update.message.reply_text(
        "Что вы хотите сделать?",
        reply_markup=reply_markup
    )


def keyboard3(update: Update, context: CallbackContext):
    keyboard = [
        [
            KeyboardButton("/search"),
            KeyboardButton(back_text)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
                                       one_time_keyboard=False)
    update.message.reply_text(
        "Начинаем поиск!",
        reply_markup=reply_markup
    )


def choice_options(update: Update, context: CallbackContext, option):
    global opt
    if option == CALLBACK_SEARCH_TRACK:
        opt = 1
        keyboard3(update=update, context=context)
    if option == CALLBACK_SEARCH_ARTIST:
        opt = 2
        keyboard3(update=update, context=context)
    if option == CALLBACK_SEARCH_ALBUM:
        opt = 3
        keyboard3(update=update, context=context)
    if option == CALLBACK_SEARCH_PLAYLIST:
        opt = 4
        keyboard3(update=update, context=context)


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