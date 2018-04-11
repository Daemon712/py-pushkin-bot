import os

from telegram.ext import Updater


def handle(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    print(error, flush=True)


def main():
    token = os.environ.get("BOT_TOKEN")
    updater = Updater(token=token)

    dp = updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(handle)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
