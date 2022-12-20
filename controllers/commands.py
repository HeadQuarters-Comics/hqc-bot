from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import os
import datetime
import pytz

from settings import TELEGRAM_ADMIN_USERNAME

from services.aws import list_folders, get_hq, list_hqs
from services.db import insert_publishers, insert_titles, update_editions, select
from services.telegram import alert_admin

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hellooooo man, Bem-vindo ao bot. Manda o comando /help pra aprender a como usar :)")

    username = update.message.from_user.username
    name = update.message.from_user.full_name    
    timezone = pytz.timezone("America/Sao_Paulo")
    alert_admin(f'{name} (@{username}) chamou o Bot às {datetime.datetime.now().astimezone(timezone).strftime("%d/%m/%Y %H:%M")}')


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Comandos disponíveis :
    /instagram - Para ver o Instagram do HQC
    /editoras - Para ver a lista de quadrinhos
    /edicoes - Para ver a quantidades de edições de um título
    /baixar - Para baixar uma edição""")


def list_publishers(update: Update, context: CallbackContext):
    publishers = select('publishers')
    print(publishers)
    keyboard = []
    print('-------------------')
    print('Editoras:')
    for publisher in publishers:
        publisher_name = publisher[1]
        print(publisher_name.upper())
        keyboard.append([InlineKeyboardButton(publisher_name.upper(), callback_data=str(publisher_name))])
    print('-------------------')


    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Escolha a editora para ver os títulos:", reply_markup=reply_markup)

def list_editions(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    name = update.message.from_user.full_name    
    timezone = pytz.timezone("America/Sao_Paulo")

    if len(context.args) == 0:
        update.message.reply_text("""Para descobrir a quantidade de edições de uma HQ, é necessário passar o título.
        \n Exemplo: /edicoes A_THOR""")
        return
    if len(context.args) != 1:
        update.message.reply_text("""⚠️ Opa, calma aí! ⚠️
        \n Verifique se mandou tudo direitinho.
        \n Você precisa passar apenas uma informação: o título.
        \n Não esqueça que o nome do título deve ter _ (underline) no lugar dos espaços :b""")
        return

    editions = select('editions', 'title', context.args[0])
    print(editions)
    if not type(editions).__name__ == 'list':
        print(f'Não achei a lista de edições. Retornou: {editions}')
        update.message.reply_text(f'Infelizmente não temos nenhuma edição desse título no momento :(')
        alert_admin(f'{name} (@{username}) Procurou por {context.args[0]} às {datetime.datetime.now().astimezone(timezone).strftime("%d/%m/%Y %H:%M")} mas infelizmente não temos :(')
        return
    title = context.args[1].upper().replace('_', ' ')
    message = f'Nós temos {len(editions)} edições de {title}: \n'
    print('-------------------')
    print('Edições:')
    for edition in editions:
        message = message + f'\n {title} #{edition[1]}.pdf'
        print(f'{title} #{edition[1]}.pdf')
    update.message.reply_text(f'{message}')
    print('-------------------')


def download(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    name = update.message.from_user.full_name    
    timezone = pytz.timezone("America/Sao_Paulo")

    if len(context.args) == 0:
        update.message.reply_text("""Para baixar uma HQ é necessário passar o título e a edição 
        \n Exemplo: /baixar A_THOR 1""")
        return
    if len(context.args) != 2:
        update.message.reply_text("""⚠️ Opa, calma aí! ⚠️
        \n Verifique se mandou tudo direitinho.
        \n Você precisa passar 2 informações: o título e o número da edição.
        \n Não esqueça que o nome do título deve ter _ (underline) no lugar dos espaços :b""")
        return

    title = (context.args[0]).lower().replace('-', '_')
    edition = context.args[1]
    print(f'Parâmentros enviados para download: {title}, {edition}')
    print(select('editions', ['identifier', 'title'], [edition, title]))
    if select('editions', ['identifier', 'title'], [edition, title]):
        publisher = select('hqs', 'name', title)
        try: 
            get_hq(publisher[0][2], title, edition)
        except Exception as error:
            print(error)
            update.message.reply_text('Sinto muito! Tivemos um erro ao buscar esse título :(')
            alert_admin(f'{name} (@{username}) Procurou por {publisher[0][2]}/{title}/{edition} às {datetime.datetime.now().astimezone(timezone).strftime("%d/%m/%Y %H:%M")} mas infelizmente não conseguimos enviar :(')
            return error 
        if os.path.exists(f'data/{title}_{edition}.pdf'):
            update.message.reply_text('Opa! Achei aqui. Só um segundo que já estou enviando...')
            hq_path = f'data/{title}_{edition}.pdf'
            new_title = f'{title.replace("_", " ").title()} #{edition}.pdf'
            #update.message.reply_document(document=open(hq_path, 'rb'), filename=new_title, timeout=1000)
        update.message.reply_text('Prontinho. Divirta-se! :D')
        print(f'HQ -> {new_title} Enviada!')
        print('-------------------')
        os.remove(hq_path)
        alert_admin(f'{name} (@{username}) Solicitou {new_title} às {datetime.datetime.now().astimezone(timezone).strftime("%d/%m/%Y %H:%M")}')
    else:
        update.message.reply_text('Poxa, ainda não temos esse título ou edição disponível para download :(')
        alert_admin(f'{name} (@{username}) Procurou por {publisher[0][2]}/{title}/{edition} às {datetime.datetime.now().astimezone(timezone).strftime("%d/%m/%Y %H:%M")} mas infelizmente não temos :(')


def sync(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    name = update.message.from_user.full_name    
    timezone = pytz.timezone("America/Sao_Paulo")

    if username == TELEGRAM_ADMIN_USERNAME:
        alert_admin(f'Iniciando sincronização com o banco...')
        update.message.reply_text('Iniciando sincronização com o banco...')

        folders = list_folders('')
        publishers = []
        for publisher in folders:
            publisher_name = str(publisher).replace('/', '')
            publishers.append(publisher_name)

        alert_admin(f'Atualizando editoras - {publishers}')
        insert_publishers(publishers)
        update.message.reply_text('Editoras atualizadas!')

        alert_admin(f'Atualizando HQs...')
        for folder in folders:
            titles_folders = list_folders(folder)
            for title in titles_folders:
                hq_name = str(title).replace(folder, '').replace('/', '')
                publisher = str(title).replace(hq_name, '').replace('/', '')
                insert_titles(hq_name, publisher)
        update.message.reply_text('HQs atualizadas!')

        alert_admin(f'Atualizando edições...')
        for folder in folders:
            titles_folders = list_folders(folder)
            for title in titles_folders:
                editions = list_hqs(title)
                title_name = str(title).replace(folder, '').replace('/', '')
                update_editions(editions, title_name)
        update.message.reply_text('Edições atualizadas!')

        alert_admin(f'Sincronização concluída!')
        update.message.reply_text('Sincronização concluída!')


    else:
        alert_admin(f'{name} @({username}) tentou usar o comando de sincronização às {datetime.datetime.now().astimezone(timezone).strftime("%d/%m/%Y %H:%M")}')
        update.message.reply_text('Você não tem permissão para usar esse comando.')


        
def hqc_instagram(update: Update, context: CallbackContext):
    update.message.reply_text(
        "HQC Comics Instagram => https://www.instagram.com/hqc.comics/")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Desculpa '%s' não é um comando válido :(" % update.message.text)