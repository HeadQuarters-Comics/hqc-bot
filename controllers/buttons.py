from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from services.aws import list_folders
from services.db import select

def publisher_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    selected = query['data']
    
    hqs = select('hqs', 'publisher', selected)
    update.callback_query.answer(f'Você selecionou {selected}')
    print(hqs)
    message = f'Da editora {str(selected).upper()} nós temos: \n'
    print(f'{str(selected).upper()}:')
    for hq in hqs:
        hq = str(hq[1]).replace(f'{selected.lower()}/', '')
        hq = str(hq).replace('/', '')
        hq = hq.replace('_', ' ')
        message = message + f'\n {hq.upper()}'
        print(hq.upper())
    update.callback_query.message.reply_text(f'{message}')
    print('-------------------')

