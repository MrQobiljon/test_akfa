'''TEXTLARNI ILADIGAN HANDLERLAR'''
from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from config import ADMINS
from keyboards.default import admin_panel_button, register_button, send_phone_button
from keyboards.inline import date_buttons_for_user
from handlers.users.commands import get_password_for_check


# ---------------------Registratsiya start-----------------------

user_info = {}
@bot.message_handler(func=lambda message: message.text == "Рўйҳатдан ўтиш")
def register(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    msg = bot.send_message(chat_id, "Ф.И.Ш. Кирил алифбосида тўлиқ киритинг\nНамуна (Азизов Азиз Азизович)",
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_user_full_name)


def get_user_full_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    user_info[from_user_id] = {
        'full_name': message.text
    }
    msg = bot.send_message(chat_id, "Телефон ракамингизни киритинг\nНамуна +998 90 900 00 00",
                           reply_markup=send_phone_button())
    bot.register_next_step_handler(msg, get_user_phone_number)


def get_user_phone_number(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    full_name = user_info[from_user_id]['full_name']
    db.save_user(full_name, phone_number, 1, from_user_id)
    bot.send_message(chat_id, "Рўйҳатдан муваффақиятли ўтдингиз", reply_markup=admin_panel_button(from_user_id))
    if db.select_dates_for_user(from_user_id):
        text = "Мажлислар санаси"
        markup = date_buttons_for_user(from_user_id)
    else:
        text = " Мажлислар санаси мавжуд емас"
        markup = admin_panel_button(from_user_id)
    bot.send_message(chat_id, text, reply_markup=markup)

    """Bu yerda majlislar sanasini chiqarishim kerak. Agar bo'lmasa, Majlislar sanasi mavjud emas degan habar chiqarishim kerak"""


# ---------------------Registratsiya end-----------------------

@bot.message_handler(func=lambda message: message.text == 'Сахифани янгилаш')
def reacton_to_sahifani_yangilash(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    try:
        logic = db.select_logic_from_user(chat_id)[0]
        if not logic:
            msg = bot.send_message(chat_id, f"Илтимос паролни киритинг",
                                   reply_markup=admin_panel_button(from_user_id))
            bot.register_next_step_handler(msg, get_password_for_check)
        else:
            user = db.select_user_by_telegram_id(telegram_id=chat_id)
            if None in user:
                bot.send_message(chat_id, "Келинг рўйҳатдан ўтиб олайлик", reply_markup=register_button())
            else:
                bot.send_message(chat_id, "Мажлислар санаси", reply_markup=date_buttons_for_user(chat_id))
    except:
        try:
            db.insert_user_telegram_id(chat_id)
        except:
            pass
        msg = bot.send_message(chat_id, f"Илтимос паролни киритинг",
                               reply_markup=admin_panel_button(from_user_id))
        bot.register_next_step_handler(msg, get_password_for_check)


@bot.message_handler(func=lambda message: message.text == 'Бекор қилиш')
def reacton_to_bekor_qilish(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    bot.send_message(chat_id, "Асосий сахифа", reply_markup=admin_panel_button(from_user_id))