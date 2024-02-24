'''
SIZ BU YERDA ODDIY KNOPKALAR YARATA OLASIZ
'''

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import db
from config import ADMINS


def register_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Рўйҳатдан ўтиш")
    markup.add(btn)
    return markup


def admin_panel_button(from_user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Сахифани янгилаш")
    markup.add(btn1)
    if from_user_id in ADMINS:
        btn2 = KeyboardButton("Админ Буйруқлари")
        markup.add(btn2)
    return markup



def delete_password_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if int(db.select_password()[1]) == 1:
        text = "Паролни вақтинчалик ўчириш"
    else:
        text = "Паролни ёқиш"
    btn1 = KeyboardButton(text)
    btn2 = KeyboardButton('Паролни бтунлай ўчириш')
    btn3 = KeyboardButton("Ортга⬅️")
    markup.add(btn1, btn2, btn3)
    return markup


def cancel_send():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Бекор қилиш")
    markup.add(btn)
    return markup


def send_phone_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Телефон ракамни юбориш", request_contact=True)
    markup.add(btn)
    return markup