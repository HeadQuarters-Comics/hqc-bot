import requests
from settings import TELEGRAM_BOT_TOKEN, HQC_CHAT_ID

def alert_admin(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={HQC_CHAT_ID}&text={message}'
    results = requests.get(url)
    print('-------------------')
    print(f'{message}')
    print(f'Avisando os administradores do HQC...')
    print('-------------------')