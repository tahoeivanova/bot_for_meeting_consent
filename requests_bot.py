import requests
import time
import pprint
from credentials import ID_dict

# создаем бота в BotFather, получаем токен
TOKEN = '1823199197:AAEkxLZoTNDaIxt0QxROHQ4FuzjlY4OYbUI'

# создем запросы к telegram  https://api.telegram.org/bot<token>/METHOD_NAME

URL_BOT = f'https://api.telegram.org/bot{TOKEN}'

# настраиваем прокси


# определяем метод

url = f'{URL_BOT}/getMe'

# делаем запрос через requests, получаем информацию о боте

# results = requests.get(url, proxies=proxies)
# print(results.json())

# что боту было написано
# метод - getUpdates
url = f'{URL_BOT}/getUpdates'
# метод отправки пользователю сообщений
url_send = f'{URL_BOT}/sendMessage'
url_contact = f'{URL_BOT}/sendContact?chat_id={ID_dict["chat_id"]}&phone_number=+79000000420&first_name=Some+Random+String'



# создаем Pool запросы
while True:
    time.sleep(3)
    results = requests.get(url_contact)
    print(results.json())
    pprint.pprint(results.json())
    # messages = results.json()['result']
    # for message in messages:
    #     # получаем написанный боту текст
    #
    #     pprint.pprint(message['message']['text'])
    #
    #     # отправим пользователю сообщение
    #     chat_id = message['message']['chat']['id']
    #     params = {
    #         'chat_id': chat_id,
    #         'text': 'Я бот, привет!'
    #     }
    #
    #     # передaем ответ с помощью метода post
    #     answer = requests.post(url_send, params=params, proxies=proxies)



