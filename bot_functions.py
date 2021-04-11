from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import ReplyKeyboardRemove
import config


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.
def echo(update: Update, context: CallbackContext):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    text = update.message.text
    if text == 'Найти трек':
        search_track(update=update, context=context)
    elif text == 'Найти исполнителя':
        search_artist(update=update, context=context)
    elif text == 'Найти альбом':
        search_album(update=update, context=context)
    elif text == 'Найти плейлист':
        search_playlist(update=update, context=context)
    elif text == 'Закрыть клавиатуру':
        close_keyboard(update=update, context=context)
    elif text == 'Дать леща':
        na_lesha(update=update, context=context)
    else:
        update.message.reply_text(f"Я получил сообщение {update.message.text}")


def search_track(update: Update, context: CallbackContext):
    update.message.reply_text("Введите название трека")
    track = update.message.reply_text


def search_artist(update: Update, context: CallbackContext):
    update.message.reply_text("Введите имя исполнителя")
    artist = update.message.reply_text


def search_album(update: Update, context: CallbackContext):
    update.message.reply_text("Введите название альбома")
    album = update.message.reply_text


def search_playlist(update: Update, context: CallbackContext):
    update.message.reply_text("Ищем плейлисты")
    playlist = update.message.reply_text


def na_lesha(track = update.message.reply_text):
    update.message.reply_text("ПОЛУЧИ ЛЕЩА")


def open_keyboard(update: Update, context: CallbackContext):
    reply_keyboard = [['Найти трек', 'Найти исполнителя'],
                      ['Найти альбом', 'Найти плейлист'], ['Дать леща', 'Закрыть клавиатуру']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(
        "Клавиатура открыта",
        reply_markup=markup)


def close_keyboard(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Клавиатура свернута",
        reply_markup=ReplyKeyboardRemove()
    )
