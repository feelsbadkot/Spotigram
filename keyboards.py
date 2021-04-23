from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove

search_text = '🔍Поиск'
help_text = '🍼Помощь'
back_text = '⬅️Назад'
back_text2 = '⬅️Вернуться к опциям'

CALLBACK_SEARCH_TRACK = '🎧Найти трек'
CALLBACK_SEARCH_ARTIST = '🎤Найти исполнителя'
CALLBACK_SEARCH_ALBUM = '🎸Найти альбом'
CALLBACK_SEARCH_PLAYLIST = '⭐️Найти плейлист'


def keyboard1():
    reply_keyboard = [[KeyboardButton(text=search_text), KeyboardButton(text=help_text)]]
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
            KeyboardButton(back_text),
            KeyboardButton(help_text)
        ],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def keyboard3():
    keyboard = [
        [
            KeyboardButton("/search"),
            KeyboardButton(back_text2)]
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
