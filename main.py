# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
import config, bot_functions


def main():
    # Создаём объект updater.
    updater = Updater(config.TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(Filters.text, bot_functions.echo)

    # Зарегистрируем их в диспетчере рядом
    # с регистрацией обработчиков текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.
    dp.add_handler(CommandHandler("start", bot_functions.start))
    dp.add_handler(CommandHandler("help", bot_functions.help))
    dp.add_handler(CommandHandler("address", bot_functions.address))
    dp.add_handler(CommandHandler("phone", bot_functions.phone))
    dp.add_handler(CommandHandler("site", bot_functions.site))
    dp.add_handler(CommandHandler("open", bot_functions.open_keyboard))
    dp.add_handler(CommandHandler("close", bot_functions.close_keyboard))
    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
