from settings import TELEGRAM_BOT_TOKEN

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import CallbackQueryHandler, ContextTypes
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from aws import list_folders, list_hqs


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hellooooo man, Bem-vindo ao bot. Manda o comando /help pra aprender a como usar :)")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /editoras - Para listar as editoras que temos atualmente
    /instagram - Para ver o Instagram do HQC""")


def list_publishers(update: Update, context: CallbackContext):
    publishers = list_folders('')
    keyboard = []
    for publisher in publishers:
        print(publisher)
        publisher_name = str(publisher).replace('/', '')
        keyboard.append([InlineKeyboardButton(publisher_name.upper(), callback_data=str(publishers.index(publisher)))])


    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def hqc_instagram(update: Update, context: CallbackContext):
    update.message.reply_text(
        "HQC Comics Instagram => https://www.instagram.com/hqc.comics/")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


def main() -> None:
    print('Run the bot.')
    updater = Updater(TELEGRAM_BOT_TOKEN,
                  use_context=True)
                  
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('instagram', hqc_instagram))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('editoras', list_publishers))
    updater.dispatcher.add_handler(CallbackQueryHandler('button', button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # Filters out unknown commands
    
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

    updater.start_polling()


if __name__ == "__main__":
    main()
