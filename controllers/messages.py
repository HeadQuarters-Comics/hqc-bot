from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Desculpe, eu não consegui entender você , você disse '%s'" % update.message.text)