# Импортируем необходимые классы
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from config import *
from bot_functions import *


def main():
    updater = Updater(
        token=TOKEN,
        use_context=True
    )
    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[CommandHandler("search", search)],

        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает название трека и начинает искать его.
            1: [MessageHandler(Filters.text, search_track, pass_user_data=True)],
            # Функция читает имя исполнителя и начинает искать его.
            2: [MessageHandler(Filters.text, search_artist, pass_user_data=True)],
            # Функция читает название альбома и начинает искать его.
            3: [MessageHandler(Filters.text, search_album, pass_user_data=True)],
            # Функция читает название плейлиста и начинает искать его.
            4: [MessageHandler(Filters.text, search_playlist, pass_user_data=True)],

        },

        # Точка прерывания диалога.
        fallbacks=[CommandHandler('help', help)])
    dp.add_handler(conv_handler)
    # Зарегистрируем их в диспетчере рядом
    # с регистрацией обработчиков текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("search_track", search_track))
    dp.add_handler(CommandHandler("search_artist", search_artist))
    dp.add_handler(CommandHandler("search_album", search_album))
    dp.add_handler(CommandHandler("search_playlist", search_playlist))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("open", keyboard1))
    dp.add_handler(CommandHandler("close", close_keyboard))
    #dp.add_handler(CallbackQueryHandler(keyboard_callback_handler))
    dp.add_handler(text_handler)
    # Регистрируем обработчик в диспетчере.
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
