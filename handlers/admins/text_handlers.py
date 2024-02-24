'''TEXTLARNI ILADIGAN HANDLERLAR'''
from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.default import (admin_panel_button, delete_password_buttons)
from keyboards.inline import (all_users_buttons, admin_commands_button)
from config import ADMINS


@bot.message_handler(func=lambda message: message.text == "Админ Буйруқлари")
def admin_panel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    # print('test')
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())