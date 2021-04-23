from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove

SEARCH_TEXT = '🔍Поиск'
HELP_TEXT = '🍼Помощь'
BACK_TEXT = '⬅️Назад'
BACK_TEXT2 = '⬅️Вернуться к опциям'

CALLBACK_SEARCH_TRACK = '🎧Найти трек'
CALLBACK_SEARCH_ARTIST = '🎤Найти исполнителя'
CALLBACK_SEARCH_ALBUM = '🎸Найти альбом'
CALLBACK_SEARCH_PLAYLIST = '⭐️Найти плейлист'
CALLBACK_SEARCH_NOVELTY = '🤡Новинки'


def keyboard1():
    reply_keyboard = [[KeyboardButton(text=SEARCH_TEXT), KeyboardButton(text=HELP_TEXT)]]
    return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)


def keyboard2():
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
            KeyboardButton(BACK_TEXT),
            KeyboardButton(CALLBACK_SEARCH_NOVELTY)
        ],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def keyboard3():
    keyboard = [
        [
            KeyboardButton("/search"),
            KeyboardButton(BACK_TEXT2)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def close_keyboard():
    return ReplyKeyboardRemove()


def inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    return InlineKeyboardMarkup(keyboard)
