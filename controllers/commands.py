from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from services.aws import list_folders

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hellooooo man, Bem-vindo ao bot. Manda o comando /help pra aprender a como usar :)")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Comandos disponíveis :-
    /editoras - Para ver a lista de quadrinhos
    /instagram - Para ver o Instagram do HQC""")


def list_publishers(update: Update, context: CallbackContext):
    publishers = list_folders('')
    keyboard = []
    for publisher in publishers:
        print(publisher)
        publisher_name = str(publisher).replace('/', '')
        keyboard.append([InlineKeyboardButton(publisher_name.upper(), callback_data=str(publisher_name))])


    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Escolha a editora para ver os títulos:", reply_markup=reply_markup)

def hqc_instagram(update: Update, context: CallbackContext):
    update.message.reply_text(
        "HQC Comics Instagram => https://www.instagram.com/hqc.comics/")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Desculpa '%s' não é um comando válido :(" % update.message.text)