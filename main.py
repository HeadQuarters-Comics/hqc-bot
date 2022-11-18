from settings import TELEGRAM_BOT_TOKEN

from telegram.ext.updater import Updater
from telegram.ext import CallbackQueryHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from controllers.buttons import publisher_button
from controllers.messages import unknown_text
from controllers.commands import start, hqc_instagram, list_publishers, unknown, help, download


def main() -> None:
    print('Running bot...')
    updater = Updater(TELEGRAM_BOT_TOKEN,
                  use_context=True)
                  
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('instagram', hqc_instagram))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('editoras', list_publishers))
    updater.dispatcher.add_handler(CommandHandler('baixar', download))
    updater.dispatcher.add_handler(CallbackQueryHandler(publisher_button))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # Filters out unknown commands
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
