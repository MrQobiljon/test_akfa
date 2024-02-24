'''KOMANDALARNI ILADIGAN HANDLERLAR'''

from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.default import admin_panel_button, register_button
from keyboards.inline import admin_commands_button, date_buttons_for_user
from config import ADMINS



@bot.message_handler(commands=['start'], chat_types='private')
def start(message: Message):
    chat_id = message.chat.id
    db.insert_user_telegram_id(chat_id)
    # if chat_id in ADMINS:
    markup = admin_panel_button(chat_id)
    # else:
    #     markup = None

    logic = db.select_logic_from_user(chat_id)[0]
    if not logic:
        msg = bot.send_message(chat_id, f"Ассалому алейкум илтимос паролни киритинг", reply_markup=markup)
        bot.register_next_step_handler(msg, get_password_for_check)
    else:
        user = db.select_user_by_telegram_id(telegram_id=chat_id)
        if None in user:
            bot.send_message(chat_id, "Келинг рўйҳатдан ўтиб олайлик", reply_markup=register_button())
        else:
            # bot.send_message(chat_id, "Мажлислар санаси", reply_markup=date_buttons_for_user(chat_id))
            bot.send_message(chat_id, "Асосий сахифа", reply_markup=admin_panel_button(chat_id))


def get_password_for_check(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if from_user_id in ADMINS:
        markup = admin_panel_button(from_user_id)
    else:
        markup = ReplyKeyboardRemove()

    if message.text == "Админ Буйруқлари":
        bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())
    else:

        try:
            password, logic = db.select_password()
            if int(logic) == 1:
                if str(message.text) == str(password):
                    db.update_logic_on_users(1, from_user_id)
                    user = db.select_user_by_telegram_id(telegram_id=from_user_id)
                    if None in user:
                        bot.send_message(chat_id, "Келинг рўйҳатдан ўтиб олайлик", reply_markup=register_button())
                    else:
                        bot.send_message(chat_id, "Асосий сахифа", reply_markup=markup)
                else:
                    msg = bot.send_message(chat_id, "Парол нотўгри кайта киритинг", reply_markup=markup)
                    bot.register_next_step_handler(msg, get_password_for_check)
            else:
                msg = bot.send_message(chat_id, "Парол нотўгри кайта киритинг", reply_markup=markup)
                bot.register_next_step_handler(msg, get_password_for_check)
        except:
            msg = bot.send_message(chat_id, "Парол нотўгри кайта киритинг", reply_markup=markup)
            bot.register_next_step_handler(msg, get_password_for_check)