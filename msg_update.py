import telebot
from datetime import time
from io import StringIO
from telebot import types
import logging
from credentials import token, ID_dict

logger = logging.getLogger(__name__)
# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(token)
mes_of_consent = 'Могу пригласить в группу еще участников?'
mes_ask = 'Приветики всем! Готовы повторить?)'
msg_8 = 'Вы все решили без меня... Мне грустно... Я спал...'
msg_9 = ''

answers = ["Нет", "Дааа"]
# ID

# сообщение
# msg = 'Привет! Я бот! Меня зовут WsyBot!\nЯ появился в эту бессонную ночь!\nЯ еще маленький и нигде не развернут, меня отрубает все что угодно, например, отсутсвие электричества.\n\n' \
#       'Kогда я работаю, я запомниаю встречи, и ты можешь смотреть и редактировать их список\n\n' \
#       'P.S. Пока не очень адаптировался в чате, лучше один на один\n'
#
# msg2 = 'Адаптировался в чате!\nМожно создавать и удалять встречи через чат!\nХорошего и доброго дня!'

# @bot.message_handler(content_types=['text'])
# def consent_do_add():
#     keyboard = types.InlineKeyboardMarkup()
#     btn_tmp = []
#     for answer in answers:
#         btn = types.InlineKeyboardButton(text=answer,
#                                          callback_data=answer)
#         btn_tmp.append(btn)
#     keyboard.add(*btn_tmp)  # кнопки с датами и днями недели
#     # bot.reply_to(message, mes_of_consent, reply_markup=keyboard)
#     bot.send_message(chat_id=ID_dict["chat_id"], text=mes_ask, reply_markup=keyboard)


#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     if call.message:
#         try:
#             if call.data in answers:
#                 bot.send_message(chat_id=ID_dict["natalia_id"], text=f'#1 {call.message.chat.username}\n{mes_of_consent}\n{call.data}')
#                 logging.debug('Sent message 1')
#         except Exception as e:
#             logging.error("Exception occurred", exc_info=True)
#
#     else:
#         logging.warning(f'No callback')



# # делаем рассылку при запуске скрипта
#
# # for i in ID_dict.values():
# #         send_welcome(i)
#
img_file = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5HgxIacBsBJ1sgyq-XMt_mvwooZ_Ruc5DVA&usqp=CAU'
# # узнать id чата
@bot.message_handler(content_types=['text'])
def send_welcome():
    # bot.send_message(ID_dict["chat_id"], msg6)
    # img_file = '/Users/Eliot/Downloads/photo5330186953188029780.jpg'
    # im = StringIO(img_file.read())
    # bot.send_photo(ID_dict['chat_id'], photo=open(img_file, 'rb'), caption='Арт-среда 0001_01')
    # bot.send_audio(chat_id=ID_dict["chat_id"], audio=open('/Users/Eliot/Downloads/sbpch_-_komnata_(vmuzone.com).mp3', 'rb'))

    # bot.send_message(ID_dict['chat_id'], text=msg_8) # (id чата, сообщение)
    bot.send_photo(ID_dict['chat_id'], photo=img_file, caption='Фото_0001_02')

    # bot.send_photo(ID_dict['chat_id'], photo=open(img_file, 'rb'), caption='Арт-среда 0001_02')

# print(message.chat.id)
# # send_welcome()
try:
    send_welcome()
except Exception as e:
    logging.error("Exception occurred", exc_info=True)
    # logging.warning(f'Exception: {e}')

# bot.polling(none_stop=True, interval=0)
