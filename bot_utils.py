import telebot
from telebot import types

def create_buttons_from_list(data_list, callback_tag=None):
    btn_lst = []
    keyboard = types.InlineKeyboardMarkup()

    for item in data_list:
        if callback_tag:
            btn = types.InlineKeyboardButton(text=f"{item}", callback_data=f'{callback_tag}_{item}')
        else:
            btn = types.InlineKeyboardButton(text=f"{item}", callback_data=f'{item}')
        btn_lst.append(btn)
    keyboard.add(*btn_lst)
    return keyboard