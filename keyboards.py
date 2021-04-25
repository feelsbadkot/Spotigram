from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove
from config import *
# файл со всеми экземплярами клавиатур


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


def back_keyboard():
    keyboard = [
        [
            KeyboardButton(BACK_TEXT2)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def close_keyboard():
    return ReplyKeyboardRemove()
