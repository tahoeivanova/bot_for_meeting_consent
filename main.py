import emoji
import telebot
from datetime import datetime
import time
from telebot import types
from mongo_db_cluster import db
import random
import re
# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from lists import hello, send_love, love_sticker, stopwords, plans, sticker_ok, sticker_music, sticker_who_i_am, filters, need_you_bot, sleep_sticker, sleep, sticker_list, img_list
from calendar_for_btn import nearest_7_days, iterate_over_hours, validate_data
import pprint
from credentials import ID_dict,token


from emodji_unicode import EMOJI_UNICODE_ENGLISH
from bot_utils import create_buttons_from_list

import logging

logger = logging.getLogger(__name__)
# Create handlers
# c_handler = logging.StreamHandler()
c_handler = logging.FileHandler('file.log')
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




message_when = None
message_what = None
message_time = None

data_to_delete_test = ''
pofigisy = 0
user_data_to_delete = ''
data_to_delete = 0
user_dict = dict()
from_user_id = None
username = None



what_to_do = ['MEET']
users_answered_yes = 0
answers = ["Ни за что", 'Да', 'Пофиг']



bot = telebot.TeleBot(token)

# ответ бота на команды /start /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message,
    "Низкоуровневая работа со временем\n"
    "/what  -  чем займемся (в разработке)\n"
    "/meet  -  список встреч\n"
    "/delete  -  удаляю встречу\n"
    '/help  -  открываю помощь\n\n'
    )

@bot.message_handler(commands = ['why_me'])
def description(message):
    bot.reply_to(message, 'Триангулирую отношения в вопросах пространства и времени')

@bot.message_handler(func=lambda message: str(message.chat.id) not in list(ID_dict.values()))
@bot.message_handler(commands=['what'])
def tell_me_what(message):
    global from_user_id
    global username

    from_user_id = message.from_user.id
    username = message.from_user.username

    user_dict[from_user_id] = dict()
    # user_dict[from_user_id]['name'] = from_user_id
    print(user_dict)

    keyboard = create_buttons_from_list(what_to_do)
    bot.reply_to(message, 'Чем займемся?', reply_markup=keyboard)

@bot.message_handler(func=lambda message: str(message.chat.id) not in list(ID_dict.values()))
@bot.message_handler(commands=['when'])
def tell_me_when(message):
    global message_when
    message_when = message.id


    try:
        global from_user_id
        global username
        if from_user_id is None:
            from_user_id = message.from_user.id
        if username is None:
            username = message.from_user.username
        btn_lst = []
        keyboard = types.InlineKeyboardMarkup()
        year = list(nearest_7_days())[0].strftime("%Y") # Выводим в сообщение год
        month = list(nearest_7_days())[0].strftime("%B") # Выводим в сообщение месяц
        days_iteration = [date for date in nearest_7_days() if date.weekday() != 5]
        for chosen_date in days_iteration: # итерируемся по списку из ближайших 7 дней
            btn = types.InlineKeyboardButton(text=f'{chosen_date.strftime("%a")} {chosen_date.day}',
                                             callback_data=chosen_date.strftime("%Y-%B-%d-%a"))
            btn_lst.append(btn)
        keyboard.add(*btn_lst) # кнопки с датами и днями недели
        bot.reply_to(message, f'{year} {month}', reply_markup=keyboard) # Выводим год и месяц с кнопками


    except:
        bot.reply_to(message, 'ooops')


def choose_time(message):
    try:
        global message_what
        bot.delete_message(message.chat.id, message_what)
        print(message_what)

        # print(message.chat.id)
        global from_user_id
        date = user_dict[from_user_id]['datetime'] # Находим в словаре выбранную дату в формате datetime
        keyboard = types.InlineKeyboardMarkup() # Создаем кнопки со временем
        btn_lst = []
        # # 6 index of timetuple -  # weekday (0 = Monday)
        hours_in_day = []
        if (date.timetuple()[6] == 1) or (date.timetuple()[6] == 4):
            hours_in_day = iterate_over_hours(date, start=8, stop=10)
        elif (date.timetuple()[6] == 0):
            hours_in_day = iterate_over_hours(date, start=13, stop=20)
        elif date.timetuple()[6] == 6:
            hours_in_day = iterate_over_hours(date, start=10, stop=22)
        else:
            hours_in_day = iterate_over_hours(date)


        for chosen_time in hours_in_day: # Итерируемся по часам
            time_to_print = chosen_time.strftime("%H:%M")
            # time_to_print = datetime.strptime(f'{chosen_time.hour}:{chosen_time.minute}0', "%H:%M")
            btn = types.InlineKeyboardButton(text=f'{time_to_print}',
                                             callback_data=time_to_print)
            btn_lst.append(btn)
        keyboard.add(*btn_lst)
        # Выводим опрос
        # bot.
        bot.reply_to(message, f'Дата: {date.strftime("%Y-%B-%d-%a")}', reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, 'ooops')
        print(e)

@bot.message_handler(func=lambda message: str(message.chat.id) not in list(ID_dict.values()))
@bot.message_handler(commands=['all'])
def all_meetings(message):
    if message.from_user.id == ID_dict["natalia_id"]:
        try:
            docs = db.when_where.find({},{"_id":0, "name": 1,  "username": 1, "what_date_time":1})
            tmp_list = []
            for document in docs:
                username = document['username']
                datetimes = [{k:v.strftime("%Y-%B-%d-%a %H:%M") for k, v in d.items()}for d in document['what_date_time']]
                tmp_list.append(f'{username}\n{datetimes}')

            dicts = '\n'.join(tmp_list)
            bot.reply_to(message, dicts)
        except Exception as e:
            bot.reply_to(message, e)


def show_dates(message):
    try:
        myquery = {"name": message.from_user.id}
        obj = db.when_where.find_one(myquery)
        datetimes = obj['datetime']
        datetimes = [d.strftime("%Y-%B-%d-%a %H:%M") for d in datetimes]
        datetimes = '\n'.join(datetimes)
        bot.send_message(message.from_user.id, datetimes) # Выводим год и месяц с кнопками
    except Exception as e:
        bot.send_message(message.from_user.id, f'oops\nno dates') # Выводим год и месяц с кнопками

@bot.message_handler(func=lambda message: str(message.chat.id) not in list(ID_dict.values()))
@bot.message_handler(commands=['meet'])
def show_dates_we_meet(message):
    try:
        myquery = {"name": message.from_user.id}
        obj = db.when_where.find_one(myquery)
        datetimes = obj['what_date_time']
        str = ''
        for item in datetimes:
            str +=f'{list(item.keys())[0]} {list(item.values())[0].strftime("%Y-%B-%d-%a %H:%M")}\n'


        # datetimes_list = [{k:v.strftime("%Y-%B-%d-%a %H:%M") for k, v in d.items()} for d in datetimes]
        #
        # print(datetimes_list)
        #

        # datetimes = [d.strftime("%Y-%B-%d-%a %H:%M") for d in datetimes]
        # datetimes = '\n'.join(datetimes)
        bot.reply_to(message, str) # Выводим год и месяц с кнопками
    except Exception as e:
        bot.send_message(message.from_user.id, f'{e}\nno dates') # Выводим год и месяц с кнопками


@bot.message_handler(func=lambda message: str(message.chat.id) not in list(ID_dict.values()))
@bot.message_handler(commands=['delete'])
def delete_date(message):
    try:
        global from_user_id
        from_user_id = message.from_user.id


        myquery = {"name": message.from_user.id}
        obj = db.when_where.find_one(myquery)
        datetimes = obj['what_date_time']
        # print(datetimes)
        # datetimes = [d.strftime("%Y-%B-%d-%a %H:%M") for d in datetimes]
        btn_lst = []
        keyboard = types.InlineKeyboardMarkup()

        for item in datetimes:  # итерируемся по списку из ближайших 7 дней
            text = f'{list(item.keys())[0]} {list(item.values())[0].strftime("%B-%d-%a %H:%M")}\n'
            btn = types.InlineKeyboardButton(text=f'{text}',
                                             callback_data=f'delete_{text}')
            btn_lst.append(btn)
        keyboard.add(*btn_lst)  # кнопки с датами и днями недели
        bot.reply_to(message, f'Нажмите, чтобы удалить', reply_markup=keyboard)  # Выводим год и месяц с кнопками

    except Exception as e:
        bot.send_message(message.from_user.id, f'oops\nsmth went wrong')  #

@bot.message_handler(func=lambda message: str(message.chat.id) not in list(ID_dict.values()))
@bot.message_handler(commands=['add_me'])
def get_chat_members(message):
    users = db.users
    query = list(users.find({"user_id": message.from_user.id}, {"user_id": 1, "username": 1, "_id": 0}))
    if query:
        bot.send_message(message.from_user.id, f'username: {query[0]["username"]}\nuser_id: {query[0]["user_id"]}')

    else:
        info = bot.get_chat_member(ID_dict['chat_id'], message.from_user.id) # данные о юзере из чата
        doc = {'user_id': info.user.id,
               'username': info.user.username}
        try:
            users.insert_one(doc)
            bot.send_message(message.from_user.id, f'username: {doc["username"]}\nuser_id: {doc["user_id"]}')
            logging.debug('New registration')

        except:
            logging.error("Exception occurred", exc_info=True)



@bot.message_handler(func=lambda message: str(message.chat.id) not in list(ID_dict.values()))
@bot.message_handler(content_types=['text', 'sticker'])
def send_messages(message):
    try:
        if message.sticker:
            time.sleep(3)
            sticker = random.choice(sticker_list)
            bot.send_sticker(message.chat.id, sticker)
        elif message.photo:
            time.sleep(3)
            img = random.choice(img_list)
            # принимаем стикер и запоминаем его id
            bot.send_photo(message.chat.id, img)
        elif message.text in EMOJI_UNICODE_ENGLISH.values():
            bot.reply_to(message, f'{emoji.emojize("Evrth is :red_heart:",variant="emoji_type")}')
        else:

            if any([(x in message.text.lower()) for x in plans]) and (("бот" in message.text.lower()) or ("wsy" in message.text.lower())  or ("bot" in message.text.lower())):
                bot.reply_to(message, "Я гуляю..")
            elif any([(x in message.text.lower()) for x in hello]) and (("бот" in message.text.lower()) or ("wsy" in message.text.lower())  or ("bot" in message.text.lower())):      # проверяем слова приветствия
                bot.reply_to(message, "Приветики! :-)")                             # вызываем функцию с кнопками с предложеним начать поиск картины
            elif any([(x in message.text.lower() in message.text.lower()) for x in send_love]) and (("бот" in message.text.lower()) or ("wsy" in message.text.lower())  or ("bot" in message.text.lower())):   # проверяем слова на похвалу и признания в любви
                bot.send_sticker(message.chat.id, love_sticker)    # отвечаем стикером с сердечком
            elif any([x in message.text.lower()in message.text.lower() for x in stopwords]):
                bot.reply_to(message, "хмм... ")
            elif 'ок' in message.text.lower().split() or 'ok' in message.text.lower() or 'хорошо' in message.text.lower() and (("бот" in message.text.lower()) or ("wsy" in message.text.lower())  or ("bot" in message.text.lower())):
                bot.send_sticker(message.chat.id, sticker_ok)   
            elif any([(x in message.text.lower()) for x in need_you_bot]) and (
                    ("бот" in message.text.lower()) or ("wsy" in message.text.lower()) or ("bot" in message.text.lower())):
                bot.send_sticker(message.chat.id, "Я тут, я все проспал?")
            elif any([(x in message.text.lower()) for x in sleep]) and (
                    ("бот" in message.text.lower()) or ("wsy" in message.text.lower()) or ("bot" in message.text.lower())):
                bot.send_sticker(message.chat.id, sleep_sticker)
            else:
                text = f'{message.text.lower()}'
                text = text.translate(str.maketrans(' ',' ',filters))
                print(text)

                if 'бот' in text.split() or 'bot' in text.split() or 'wsy' == text:
                    bot.send_sticker(message.chat.id, sticker_who_i_am)    # отвечаем стикером с сердечком
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)


# # КНОПОЧКИ КНОПОЧКИ КНОПОЧКИ КНОПОЧКИ
# @bot.inline_handler(lambda query: query.query =='text')
# def default_query(inline_query):
#     try:
#         # r = types.InlineQueryResultArticle('1', 'default', types.InputTextMessageContent('default'))
#         bot.answer_inline_query(inline_query.id, 'ok')
#     except Exception as e:
#         print(e)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        global from_user_id
        global username
        global user_data_to_delete
        global data_to_delete
        global message_when
        global users_answered_yes
        global pofigisy
        global message_time
        global message_what
        global data_to_delete_test

        # print(call.message.chat.id)
        # print(call.message.chat.username)
        # print(call.message.from_user.id)



        try:

            if call.data == 'Ни за что':
                if call.message.chat.id == ID_dict['chat_id']:

                    if call.from_user.username:
                        bot.answer_callback_query(call.id, f'Не проводите без {call.from_user.username} \n{data_to_delete}\nПредлагаю время \what')
                    else:
                        bot.answer_callback_query(call.id, f'Не проводите без {call.from_user.id} \n{data_to_delete}\nПредлагаю время \what.')
                    myquery = {"name": user_data_to_delete}
                    obj = db.when_where.find_one(myquery)


                    for item in obj['what_date_time']:
                        text = '{list(item.keys())[0]} {list(item.values())[0].strftime("%B-%d-%a %H:%M")}\n'
                        print('Found to delete')
                        if text == data_to_delete:
                            obj['what_date_time'].remove(item)
                    # obj['what_date_time'].remove(datetime.strptime(data_to_delete, "%Y-%B-%d-%a %H:%M"))
                    # newvalues = {"$set": {"datetime": obj['datetime']}}
                    newvalues = {"$set": {"what_date_time": obj['what_date_time']}}

                    db.when_where.update_one(myquery, newvalues)
                    bot.reply_to(call.message, f'{call.from_user.username} Только не \n{data_to_delete}\nПредлагаю время /what')
                else:
                    if call.from_user.username:
                        bot.answer_callback_query(call.id, f'{call.from_user.username} Только не \n{data_to_delete_test}\nПредлагаю время /what')
                    else:
                        bot.answer_callback_query(call.id, f'{call.from_user.id} Только не \n{data_to_delete_test}\nПредлагаю время /what')


                    myquery = {"name": from_user_id}
                    obj = db.when_where.find_one(myquery)

                    for item in obj['what_date_time']:
                        text = '{list(item.keys())[0]} {list(item.values())[0].strftime("%B-%d-%a %H:%M")}\n'
                        print('Found to delete')
                        if text == data_to_delete_test:
                            obj['what_date_time'].remove(item)
                    # obj['what_date_time'].remove(datetime.strptime(data_to_delete, "%Y-%B-%d-%a %H:%M"))
                    # newvalues = {"$set": {"datetime": obj['datetime']}}
                    newvalues = {"$set": {"what_date_time": obj['what_date_time']}}

                    db.when_where.update_one(myquery, newvalues)
                    bot.reply_to(call.message, f'{call.from_user.username} Только не {data_to_delete_test}\nПредлагаю время /what.')

                # bot.send_message(call.message.chat.id, '/meet')
                #             bot.send_message(chat_id=ID_dict["natalia_id"], text=f'#1 {call.message.chat.username}\n{mes_of_consent}\n{call.data}')
                #             logging.debug('Sent message 1')
            elif call.data == 'Пофиг':
                if call.message.chat.id == ID_dict["chat_id"]:
                    if call.from_user.username:
                        bot.answer_callback_query(call.id, f'Устраивает {call.from_user.username} \n{data_to_delete}')
                    else:
                        bot.answer_callback_query(call.id, f'Устраивает {call.from_user.id} \n{data_to_delete}')
                    if call.from_user.username:

                        print(call.from_user.username, 'Пофиг')
                    pofigisy += 1
                    if pofigisy + users_answered_yes == 8:
                        bot.reply_to(call.message, f'{users_answered_yes} человек устраивает \n{data_to_delete}')
                else:
                    if call.from_user.username:
                        bot.answer_callback_query(call.id, f'Устраивает {call.from_user.username} \n{data_to_delete_test}')
                    else:
                        bot.answer_callback_query(call.id, f'Устраивает {call.from_user.id} \n{data_to_delete_test}')
                    bot.reply_to(call.message, f'Устраивает \n{data_to_delete_test}')



            elif call.data == 'Да':


                if call.message.chat.id == ID_dict["chat_id"]:

                    if call.from_user.username:

                        print(call.from_user.username, 'Да')
                    if call.from_user.username:
                        bot.answer_callback_query(call.id, f'Устраивает {call.from_user.username} \n{data_to_delete}')
                    else:
                        bot.answer_callback_query(call.id, f'Устраивает {call.from_user.id} \n{data_to_delete}')

                    users_answered_yes+=1
                    if pofigisy + users_answered_yes == 8:
                        bot.reply_to(call.message, f'{users_answered_yes} человек устраивает \n{data_to_delete}')
                else:
                    print(call.from_user.id)
                    # print(call.id)
                    # print(call.message.from_user.id)
                    if call.from_user.username:
                        bot.answer_callback_query(call.id, f'Устраивает {call.from_user.username} \n{data_to_delete_test}')
                    else:
                        bot.answer_callback_query(call.id, f'Устраивает {call.from_user.id} \n{data_to_delete_test}')


                    call_back_query = bot.answer_callback_query(callback_query_id=call.id, text=f'ок')
                    print(call_back_query)


                    # bot.reply_to(call.message, f'Устраивает \n{data_to_delete}')



            elif call.data in what_to_do:

                user_dict[from_user_id]['what_to_do'] = call.data
                message_what = call.message.id

                # db.what_to_do.insert({"user_id": from_user_id, "username": username, 'what_to_do': call.data.lstrip("what_to_do_")})
                tell_me_when(call.message)
                # bot.register_next_step_handler(call.message, tell_me_when)
            elif validate_data(call.data, "%H:%M"): # Если выбрано время
                bot.delete_message(call.message.chat.id, message_when)

                # print(user_dict[from_user_id]['what_to_do'])
                what_to_do_item = user_dict[from_user_id]['what_to_do']


                # Запоминаем в словарь время, преобразованное в datetime из строки (пример 2021-06-05 00:00:00)
                dt = datetime.combine(user_dict[from_user_id]['datetime'], datetime.strptime(call.data, "%H:%M").time())
                if call.message.chat.id == ID_dict["chat_id"]:
                    data_to_delete = dt
                else:
                    data_to_delete_test = dt



                # Добавляем в бд
                myquery = {"name": from_user_id}
                try:
                    mydoc = db.when_where.find(myquery)
                except:
                    mydoc = []
                if list(mydoc) == []:
                    dict_to_db = {"name": from_user_id, "username": username, "what_date_time": [{what_to_do_item: dt}]}
                    # print(dict_to_db)
                    db.when_where.insert_one(dict_to_db)
                else:
                    # update
                    myquery = {"name": from_user_id}
                    obj = db.when_where.find_one(myquery)
                    datetime_change = obj['what_date_time']
                    if dt not in datetime_change:
                        datetime_change.append({what_to_do_item: dt})
                        # print(obj)
                        # print(type(obj))
                        newvalues = {"$set": {"what_date_time": datetime_change}}

                        db.when_where.update_one(myquery, newvalues)
                    # dict_to_db = {"name": call.message.chat.id, "datetime": [dt]}

                #
                #
                # db.when_where.insert_one(dict_to_db)
                # выводим пользователю

                # '''Добавить опрос'''
                keyboard = types.InlineKeyboardMarkup()

                btn_tmp = []
                for answer in answers:
                    btn = types.InlineKeyboardButton(text=answer,
                                                     callback_data=answer)
                    btn_tmp.append(btn)
                keyboard.add(*btn_tmp)  # кнопки с датами и днями недели
                if call.message.chat.id == ID_dict['chat_id']:

                    user_data_to_delete = from_user_id



                bot.reply_to(call.message,
                             f'Удобно ли такое время?\n{user_dict[from_user_id]["what_to_do"]} {dt.strftime("%Y-%B-%d-%a %H:%M")}', reply_markup=keyboard)

                bot.delete_message(call.message.chat.id, call.message.id)





            elif validate_data(call.data, "%Y-%B-%d-%a"): # Если это выбранная дата
                message_when = call.message.id
                # bot.sendMessage(_.id, `Selected
                # '${msg.data}'
                # `);
                # bot.deleteMessage(_.id, msg.message.message_id);
                # Запоминаем в словарь дату, преобразованную в datetime из строки (пример 2021-06-05 00:00:00)
                user_dict[from_user_id]['datetime'] = datetime.strptime(call.data, "%Y-%B-%d-%a")

                choose_time(call.message) # Переходим к выбору времени
            elif 'delete_' in call.data:
                print(from_user_id)
                data_to_delete = call.data.lstrip('delete_')

                myquery = {"name": from_user_id}
                obj = db.when_where.find_one(myquery)
                for item in obj['what_date_time']:
                    text = '{list(item.keys())[0]} {list(item.values())[0].strftime("%B-%d-%a %H:%M")}\n'
                    print('Found to delete')
                    if text == data_to_delete:
                        obj['what_date_time'].remove(item)
                # obj['what_date_time'].remove(datetime.strptime(data_to_delete, "%Y-%B-%d-%a %H:%M"))
                # newvalues = {"$set": {"datetime": obj['datetime']}}
                newvalues = {"$set": {"what_date_time": obj['what_date_time']}}


                db.when_where.update_one(myquery, newvalues)
                bot.send_message(call.message.chat.id, '/meet')

            # try:
            #     if call.data in answers:
            #
            #         bot.send_message(chat_id=ID_dict["natalia_id"], text=f'{mes_ask}\n{call.message.from_user.username}\n{call.data}')
            #         logging.debug('Sent message')
            #         print(call.message)
            #
            # except Exception as e:
            #     logging.error("Exception occurred", exc_info=True)

            else:
                logging.warning('No callback')

        except Exception as e:
            logging.error("Exception occurred", exc_info=True)

            bot.reply_to(call.message, f'{e.args} oops\nsmth went wrong')  # Выводим год и месяц с кнопками


# @bot.message_handler(commands=['start'])
# def start_func(message): # Выбрать тип задачи
#     bot.reply_to(message, 'hello')



# @bot.message_handler(commands=['start'])
# def start(m):
#     calendar, step = DetailedTelegramCalendar().build()
#     bot.send_message(m.chat.id,
#                      f"Select {LSTEP[step]}",
#                      reply_markup=calendar)
#
#
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
# def cal(c):
#     result, key, step = DetailedTelegramCalendar().process(c.data)
#     if not result and key:
#         bot.edit_message_text(f"Select {LSTEP[step]}",
#                               c.message.chat.id,
#                               c.message.message_id,
#                               reply_markup=key)
#     elif result:
#         bot.edit_message_text(f"You selected {result}",
#                               c.message.chat.id,
#                               c.message.message_id)

bot.polling()