from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import os

from services.aws import list_folders, get_hq

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hellooooo man, Bem-vindo ao bot. Manda o comando /help pra aprender a como usar :)")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Comandos disponíveis :
    /editoras - Para ver a lista de quadrinhos
    /instagram - Para ver o Instagram do HQC
    /baixar - Para baixar uma edição""")


def list_publishers(update: Update, context: CallbackContext):
    publishers = list_folders('')
    keyboard = []
    for publisher in publishers:
        print(publisher)
        publisher_name = str(publisher).replace('/', '')
        keyboard.append([InlineKeyboardButton(publisher_name.upper(), callback_data=str(publisher_name))])


    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Escolha a editora para ver os títulos:", reply_markup=reply_markup)

def download(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("""Para baixar uma HQ é nessário passar a editora, o título e a edição 
        \n Exemplo: /baixar MARVEL A_THOR 1""")
        return
    if len(context.args) != 3:
        update.message.reply_text("""⚠️ Opa, calma aí! ⚠️
        \n Verifique se mandou tudo direitinho.
        \n Você precisa passar 3 informações: a editora, o título e o número da edição.
        \n Não esqueça que o nome do título deve ter _ (underline) no lugar dos espaços :b""")
        return
    publisher = (context.args[0]).lower()
    title = (context.args[1]).lower().replace('-', '_')
    edition = context.args[2]
    print(publisher, title, edition)
    try: 
        get_hq(publisher, title, edition)
    except Exception as error:
        print(error)
        if "404" in str(error):
            update.message.reply_text('Poxa, ainda não temos esse título disponível para download :(')    
        else:
            update.message.reply_text('Sinto muito! Tivemos um erro ao buscar esse título :(')
        return error 
    if os.path.exists(f'data/{title}_{edition}.pdf'):
        update.message.reply_text('Opa! Achei aqui. Só um segundo que já estou enviando...')
        hq_path = f'data/{title}_{edition}.pdf'
        new_title = f'{title.replace("_", " ").title()} #{edition}.pdf'
        print(hq_path)
        update.message.reply_document(document=open(hq_path, 'rb'), filename=new_title, timeout=1000)
    update.message.reply_text('Prontinho. Divirta-se! :D')
    os.remove(hq_path)
        

def hqc_instagram(update: Update, context: CallbackContext):
    update.message.reply_text(
        "HQC Comics Instagram => https://www.instagram.com/hqc.comics/")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Desculpa '%s' não é um comando válido :(" % update.message.text)