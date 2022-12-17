from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_buttons(list, desc):
    keyboard = []
    print('-------------------')
    print(f'{desc}:')
    for item in list:
        new_name = str(item).replace('/', '')
        print(new_name.upper())
        keyboard.append([InlineKeyboardButton(new_name.upper(), callback_data=str(new_name))])
    print('-------------------')

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup