from telegram import Bot
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from spotify_functions import search_for_track, search_for_artist, search_for_album, \
    search_for_playlist, return_new_releases
import logging
from config import *
from keyboards import *

# стандартный конфиг лога
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# лог-декоратор
def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка: {e}")
            raise e

    return inner


# выводиться при нажатии /help
def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Нажмите на клавиатуре поиск (если нет клавиатуры напишите /open)")


# самая первая функция, выводиться при нажатии на /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Привет я SpotiGram - твой помощник в мире музыки.\nНажимайте на поиск и погнали!',
        reply_markup=keyboard1())


# открывает клавиатуру вручную
def open_keyboard(update: Update, context: CallbackContext):
    update.message.reply_text("Клавиатура открыта", reply_markup=keyboard1())


# основной обработчик всех входящих сообщений
def echo(update: Update, context: CallbackContext):
    text = update.message.text
    if text == SEARCH_TEXT:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif text == BACK_TEXT:
        update.message.reply_text("Выберете опцию", reply_markup=keyboard1())
    elif text == BACK_TEXT2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif text == HELP_TEXT:
        help(update=update, context=context)
    elif text == CALLBACK_SEARCH_TRACK:
        choice_options(update=update, context=context, option=CALLBACK_SEARCH_TRACK)
    elif text == CALLBACK_SEARCH_ARTIST:
        choice_options(update=update, context=context, option=CALLBACK_SEARCH_ARTIST)
    elif text == CALLBACK_SEARCH_ALBUM:
        choice_options(update=update, context=context, option=CALLBACK_SEARCH_ALBUM)
    elif text == CALLBACK_SEARCH_PLAYLIST:
        choice_options(update=update, context=context, option=CALLBACK_SEARCH_PLAYLIST)
    elif text == CALLBACK_SEARCH_NOVELTY:
        search_novelty(update=update, context=context)
    else:
        update.message.reply_text(f'Я не знаю что ответить на "{update.message.text}"')
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())


# передает название трека который ввел пользователь в spoti-функцию для поисака трека
def search_track(update: Update, context: CallbackContext):
    if update.message.text == BACK_TEXT2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif update.message.text == HELP_TEXT:
        help(update=update, context=context)
    else:
        context.user_data['track'] = update.message.text
        track_list = search_for_track(context.user_data['track'])
        for song in track_list:
            update.message.reply_text(song['info'])
        update.message.reply_text("Введите другой трек или выберете другую опцию",
                                  reply_markup=keyboard3())
    return ConversationHandler.END


# передает имя исполнителя который ввел пользователь в spoti-функцию для поисака трека
def search_artist(update: Update, context: CallbackContext):
    if update.message.text == BACK_TEXT2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif update.message.text == HELP_TEXT:
        help(update=update, context=context)
    else:
        context.user_data['artists'] = update.message.text
        artists_list = search_for_artist(context.user_data['artists'])
        for artist in artists_list:
            update.message.reply_text(artist['info'])
            if artist['top_tracks']:
                update.message.reply_text('Топ треков:\n' + '\n'.join(artist['top_tracks']))
            if artist['discography']:
                update.effective_message.reply_text('Дискография:\n' +
                                                    '\n'.join(artist['discography']))
            update.message.reply_text(' - ' * 10)
        update.message.reply_text(
            "Нажмите на /search чтобы найти другого исполнителя или выберете другую опцию",
            reply_markup=keyboard3())
    return ConversationHandler.END


# передает название альбома который ввел пользователь в spoti-функцию для поисака трека
def search_album(update: Update, context: CallbackContext):
    if update.message.text == BACK_TEXT2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif update.message.text == HELP_TEXT:
        help(update=update, context=context)
    else:
        context.user_data['album'] = update.message.text
        album_list = search_for_album(context.user_data['album'])
        for album in album_list:
            update.message.reply_text(album['info'])
            update.message.reply_text("\n".join(album['tracks']))
            update.message.reply_text(' - ' * 10)
        update.message.reply_text(
            "Нажмите на /search чтобы найти другой альбом или выберете другую опцию",
            reply_markup=keyboard3())
    return ConversationHandler.END


# передает название плейлиста который ввел пользователь в spoti-функцию для поисака трека
def search_playlist(update: Update, context: CallbackContext):
    if update.message.text == BACK_TEXT2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif update.message.text == HELP_TEXT:
        help(update=update, context=context)
    else:
        context.user_data['playlist'] = update.message.text
        playlist_list = search_for_playlist(context.user_data['playlist'])
        for pl in playlist_list:
            update.message.reply_text(pl)
        update.message.reply_text(
            "Нажмите на /search чтобы найти другой плейлист или выберете другую опцию",
            reply_markup=keyboard3())
    return ConversationHandler.END


# выводит новинки по запросу(берет также из spoti-функции)
def search_novelty(update: Update, context: CallbackContext):
    if update.message.text == BACK_TEXT2:
        update.message.reply_text("Что вы хотите сделать?", reply_markup=keyboard2())
    elif update.message.text == HELP_TEXT:
        help(update=update, context=context)
    else:
        novelty_list = return_new_releases()
        for nov in novelty_list:
            update.message.reply_text(nov['info'])
            update.message.reply_text("\n".join(nov['tracks']))
            update.message.reply_text(' - ' * 10)
        update.message.reply_text("Выберете другую опцию",
                                  reply_markup=back_keyboard())
    return ConversationHandler.END


# отвечает за передачу выбранной опции в функцию search
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


# получает необходимые данные и возвращает их в обработчик сценариев
def search(update: Update, context: CallbackContext):
    if opt == 1:
        update.message.reply_text("Введите название трека", reply_markup=close_keyboard())
        return opt
    if opt == 2:
        update.message.reply_text("Введите имя исполнителя", reply_markup=close_keyboard())
        return opt
    if opt == 3:
        update.message.reply_text("Введите название альбома", reply_markup=close_keyboard())
        return opt
    if opt == 4:
        update.message.reply_text("Введите название плейлиста", reply_markup=close_keyboard())
        return opt
