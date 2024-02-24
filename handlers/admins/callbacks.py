'''CALLBACKLARNI ILADIGAN HANDLERLAR'''
import re
from datetime import datetime
from telebot.types import CallbackQuery, Message
from data.loader import bot, db
from config import ADMINS
from keyboards.default import admin_panel_button
from keyboards.inline import (save_password_button, admin_commands_button, delete_password_buttons,
                              all_users_buttons, users_for_date_buttons, date_buttons,
                              users_buttons_for_tasks, confirmation_send_document,
                              date_buttons_for_reports, users_for_edit_date_buttons,
                              date_buttons_for_edit, users_for_del_tasks_buttons, date_buttons_for_del_tasks,
                              task_buttons_for_del_tasks_, report_buttons1)




data_users_for_delete = []
DATA_DATE = {}
DATA_USER_FOR_DATE = {}
DATA_FOR_DATE = {}
users_for_date = []
data_for_file = {}

USERS_FOR_EDIT = {}

# -------------------------------Start Main menu--------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def reaction_to_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        markup = admin_panel_button(from_user_id)
    else:
        markup = None
    bot.send_message(chat_id, "Асосий сахифа", reply_markup=markup)

#-------------------------------End Main menu--------------------------------------------------------------


# -------------------------------Start View all users--------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == 'view_list_users')
def view_users_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Фойдаланувчиларни рўйхати", reply_markup=all_users_buttons())


@bot.callback_query_handler(func=lambda call: call.data == 'next_page')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, "Фойдаланувчиларни рўйхати", reply_markup=all_users_buttons(page, data_users_for_delete))


@bot.callback_query_handler(func=lambda call: call.data == 'previous_page')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, "Фойдаланувчиларни рўйхати", reply_markup=all_users_buttons(page, data_users_for_delete))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page')
def reaction_to_view_user(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")



@bot.callback_query_handler(func=lambda call: "view_user|" in call.data)
def reaction_to_view_user(call: CallbackQuery):
    user_id = call.data.split('|')[1]
    user_name = db.select_user_by_telegram_id(user_id)[0]
    bot.answer_callback_query(call.id, f"{user_name}")


@bot.callback_query_handler(func=lambda call: "s_user_for_del|" in call.data)
def reaction_to_del_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = int(call.data.split('|')[1])
    data_users_for_delete.append(user_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=all_users_buttons(page, data_users_for_delete))


@bot.callback_query_handler(func=lambda call: "s_user|" in call.data)
def reaction_to_del_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = int(call.data.split('|')[1])
    try:
        data_users_for_delete.remove(user_id)
    except:
        pass

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=all_users_buttons(page, data_users_for_delete))


@bot.callback_query_handler(func=lambda call: call.data == 'confirmation_del_users')
def reaction_confirmation_del_users(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        for user_id in data_users_for_delete:
            try:
                db.delete_user(user_id)
                db.update_ids_for_user('yes', user_id, from_user_id)
            except:
                pass
        data_users_for_delete.clear()
        bot.send_message(chat_id, "Фойдаланувчилар ўчирилди", reply_markup=admin_commands_button())


@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def reaction_to_cancel_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())

# -------------------------------Start View all users--------------------------------------------------------------



# -------------------------------Parol qo'sish--------------------------------------------------------------
data = {}
@bot.callback_query_handler(func=lambda call: call.data == 'add_password')
def admin_panel(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Паролни киритинг\n Намуна: 0000")
        bot.register_next_step_handler(msg, get_password)


@bot.callback_query_handler(func=lambda call: call.data == 'change_password')
def admin_panel(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Паролни киритинг\n Намуна: 0000")
        bot.register_next_step_handler(msg, get_password)


def get_password(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        password = message.text
        data[from_user_id] = {
            'password': password
        }
        bot.send_message(chat_id, "Паролни сақланг", reply_markup=save_password_button())


@bot.callback_query_handler(func=lambda call: call.data == 'save_password')
def admin_panel(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        try:
            password = data[from_user_id]['password']
            if db.select_password():
                old_password = db.select_password()[0]
                db.update_password(password, old_password)
                bot.send_message(chat_id, "Парол сақланди", reply_markup=admin_commands_button())
            else:
                db.insert_password(password, 1)
                del data[from_user_id]
                bot.send_message(chat_id, "Парол сақланди", reply_markup=admin_commands_button())
        except:
            msg = bot.send_message(chat_id, "Паролни киритинг\nНамуна: 0000")
            bot.register_next_step_handler(msg, get_password)

# -------------------------------Parol qo'sish tugadi--------------------------------------------------------------


# -------------------------------Parol o'chirish--------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == 'off_on_password')
def delete_password_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Керакли ҳаракатни амалга оширинг", reply_markup=delete_password_buttons())


@bot.callback_query_handler(func=lambda call: call.data == 'temporarily_disable_the_password')
def delete_password_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        password = db.select_password()[0]
        db.off_on_password(0, password)
        text = "Паролни вақтинчалик ўчирилди"
        bot.send_message(chat_id, text, reply_markup=admin_commands_button())


@bot.callback_query_handler(func=lambda call: call.data == 'enable_password')
def delete_password_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        password = db.select_password()[0]
        db.off_on_password(1, password)
        text = "Паролни ёқилди"
        bot.send_message(chat_id, text, reply_markup=admin_commands_button())


@bot.callback_query_handler(func=lambda call: call.data == 'delete_password_permanently')
def delete_password_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        password = db.select_password()[0]
        db.delete_password(password)
        text = "Парол бутунлай ўчирилди"
        bot.send_message(chat_id, text, reply_markup=admin_commands_button())

# -------------------------------Parol o'chirish tugadi--------------------------------------------------------------


# -------------------------------Start Vazifa sanasini qo'shish--------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == 'add_date_task')
def reaction_to_add_date_task(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    DATA_USER_FOR_DATE[from_user_id] = []
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Вазифа санасини киритинг\nНамуна: 14.09.2023")
        bot.register_next_step_handler(msg, add_date_task)


def add_date_task(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    date = message.text
    a = re.fullmatch(r'\d\d\.\d\d\.\d{4}', date)
    if a:
        DATA_DATE[from_user_id] = {
            'date': date
        }
        bot.send_message(chat_id, "Фойдаланувчиларни танланг", reply_markup=users_for_date_buttons())
    else:
        msg = bot.send_message(chat_id, "Сана нотўгри киритилди. Қайта киритинг\nНамуна: 14.09.2023")
        bot.register_next_step_handler(msg, add_date_task)


@bot.callback_query_handler(func=lambda call: call.data == 'next_page_for_date')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_for_date':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, "Фойдаланувчиларни рўйхати",
                         reply_markup=users_for_date_buttons(page, DATA_USER_FOR_DATE[from_user_id]))


@bot.callback_query_handler(func=lambda call: call.data == 'previous_page_for_date')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_for_date':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, "Фойдаланувчиларни рўйхати",
                             reply_markup=users_for_date_buttons(page, DATA_USER_FOR_DATE[from_user_id]))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page_for_date')
def reaction_to_view_user(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")



@bot.callback_query_handler(func=lambda call: "v_user_for_date|" in call.data)
def reaction_to_view_user(call: CallbackQuery):
    user_id = call.data.split('|')[1]
    user_name = db.select_user_by_telegram_id(user_id)[0]
    bot.answer_callback_query(call.id, f"{user_name}")


@bot.callback_query_handler(func=lambda call: "minus_user_d_del|" in call.data)
def reaction_to_del_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    DATA_USER_FOR_DATE[from_user_id].append(user_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_for_date':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=users_for_date_buttons(page, DATA_USER_FOR_DATE[from_user_id]))


@bot.callback_query_handler(func=lambda call: "plus_user_date|" in call.data)
def reaction_to_del_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    try:
        DATA_USER_FOR_DATE[from_user_id].remove(user_id)
    except:
        pass

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_for_date':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=users_for_date_buttons(page, DATA_USER_FOR_DATE[from_user_id]))


@bot.callback_query_handler(func=lambda call: call.data == 'save_users_for_date')
def reaction_confirmation_del_users(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date = DATA_DATE[from_user_id]['date']

    # db.insert_date(date, from_user_id)
    # date_id = db.select_date_id(date)[0]
    if db.select_date_id(date, from_user_id):
        date_id = db.select_date_id(date, from_user_id)[0]
    else:
        db.insert_date(date, from_user_id)
        date_id = db.select_date_id(date, from_user_id)[0]

    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        for user_id in DATA_USER_FOR_DATE[from_user_id]:
            db.insert_date_and_user(date_id, user_id, from_user_id)
        DATA_USER_FOR_DATE[from_user_id].clear()
        DATA_DATE[from_user_id].clear()
        bot.send_message(chat_id, "Маълумотлар сақланди", reply_markup=admin_commands_button())


# -------------------------------End Vazifa sanasini qo'sish--------------------------------------------------------------


# -------------------------------Start Vazifa qo'sish--------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == 'add_task')
def reaction_add_task(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        DATA_FOR_DATE[from_user_id] = {}
        bot.send_message(chat_id, 'Вазифа учун сана танланг', reply_markup=date_buttons(from_user_id))


@bot.callback_query_handler(func=lambda call: call.data == 'next_date')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_date':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, "Вазифа учун сана танланг",
                         reply_markup=date_buttons(from_user_id, page, DATA_FOR_DATE[from_user_id]))


@bot.callback_query_handler(func=lambda call: call.data == 'previous_date')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_date':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, "Вазифа учун сана танланг",
                             reply_markup=date_buttons(from_user_id, page, DATA_FOR_DATE[from_user_id]))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page_date')
def reaction_to_view_user(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_date':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")



@bot.callback_query_handler(func=lambda call: "view_date|" in call.data)
def reaction_to_view_user(call: CallbackQuery):
    user_id = call.data.split('|')[1]
    user_name = db.select_user_by_telegram_id(user_id)[0]
    bot.answer_callback_query(call.id, f"{user_name}")


@bot.callback_query_handler(func=lambda call: "minus_date|" in call.data)
def reaction_to_minus_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    DATA_FOR_DATE[from_user_id][date_id] = []
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Фойдаланувчиларни танланг", reply_markup=users_buttons_for_tasks(date_id, from_user_id))


@bot.callback_query_handler(func=lambda call: "plus_date|" in call.data)
def reaction_to_plus_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])

    try:
        del DATA_FOR_DATE[from_user_id][date_id]
    except:
        pass

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_date':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=date_buttons(from_user_id, page, DATA_FOR_DATE[from_user_id]))


@bot.callback_query_handler(func=lambda call: call.data == 'cancel_date')
def reaction_to_cancel_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    try:
        if DATA_FOR_DATE.get(from_user_id):
            del DATA_FOR_DATE[from_user_id]
        if data_for_file.get(from_user_id):
            del data_for_file[from_user_id]
    except:
        pass
    bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())



@bot.callback_query_handler(func=lambda call: call.data == 'commit_send_file')
def reaction_confirmation_del_users(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Вазифа номини киритинг")
        bot.register_next_step_handler(msg, get_file_name)


def get_file_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.text:
        data_for_file[from_user_id] = {
            'task_name': message.text
        }
        msg = bot.send_message(chat_id, "Файлни юбориш")
        bot.register_next_step_handler(msg, get_file)
    else:
        msg = bot.send_message(chat_id, "Вазифа номини киритинг")
        bot.register_next_step_handler(msg, get_file_name)


def get_file(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.document:
        # task_name = data_for_file[from_user_id]['task_name']
        file_id = message.document.file_id
        data_for_file[from_user_id]['file_id'] = file_id
        # db.insert_file(task_name, file_id, from_user_id)
        # file_int_id = db.select_id_by_file_text_id(file_id)[0]
        bot.send_message(chat_id, "Тасдикланг", reply_markup=confirmation_send_document())
    else:
        msg = bot.send_message(chat_id, "Файлни юбориш")
        bot.register_next_step_handler(msg, get_file)


@bot.callback_query_handler(func=lambda call: 'bekor_qilish|' in call.data)
def reaction_to_bekor_qilish(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    try:
        del DATA_FOR_DATE[from_user_id]
        del data_for_file[from_user_id]
    except:
        pass
    bot.send_message(chat_id, "Вазифа бекор килинди", reply_markup=admin_panel_button(from_user_id))


@bot.callback_query_handler(func=lambda call: 'vazifa_yuborish|' in call.data)
def reaction_to_vazifa_yuborish(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    task_name = data_for_file[from_user_id]['task_name']
    file_str_id = data_for_file[from_user_id]['file_id']
    db.insert_file(task_name, file_str_id, from_user_id)
    file_id = db.select_id_by_file_text_id(file_str_id)[0]
    bot.delete_message(chat_id, call.message.message_id)

    dates = DATA_FOR_DATE[from_user_id]
    for date_id, users in dates.items():
        for user_id in users:
            db.insert_file_id_date_id_user_id(file_id, date_id, user_id, from_user_id)

    del DATA_FOR_DATE[from_user_id]
    bot.send_message(chat_id, "Вазифа юборилди", reply_markup=admin_panel_button(from_user_id))

# Userlar bilan ishlash qismi

@bot.callback_query_handler(func=lambda call: 'next_page_for_task|' in call.data)
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    date_id = int(call.data.split('|')[1])

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_for_task':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, "Фойдаланувчиларни танланг",
                         reply_markup=users_buttons_for_tasks(date_id, from_user_id, page, DATA_FOR_DATE[from_user_id][date_id]))


@bot.callback_query_handler(func=lambda call: 'previous_page_for_task|' in call.data)
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    date_id = int(call.data.split('|')[1])

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_for_task':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, "Фойдаланувчиларни танланг",
                             reply_markup=users_buttons_for_tasks(date_id, from_user_id, page, DATA_FOR_DATE[from_user_id][date_id]))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page_for_task')
def reaction_to_view_user(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")


@bot.callback_query_handler(func=lambda call: "user_for_task|" in call.data)
def reaction_to_view_user(call: CallbackQuery):
    user_id = call.data.split('|')[1]
    user_name = db.select_user_by_telegram_id(user_id)[0]
    bot.answer_callback_query(call.id, f"{user_name}")


@bot.callback_query_handler(func=lambda call: "minus_user_task|" in call.data)
def reaction_to_del_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    date_id = int(call.data.split('|')[2])

    DATA_FOR_DATE[from_user_id][date_id].append(user_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_for_task':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=users_buttons_for_tasks(date_id, from_user_id, page, DATA_FOR_DATE[from_user_id][date_id]))


@bot.callback_query_handler(func=lambda call: "plus_user_task|" in call.data)
def reaction_to_del_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    date_id = int(call.data.split('|')[2])

    try:
        DATA_FOR_DATE[from_user_id][date_id].remove(user_id)
    except:
        pass

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_for_task':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=users_buttons_for_tasks(date_id, from_user_id, page, DATA_FOR_DATE[from_user_id][date_id]))


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_date')
def reaction_back_to_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'Санани танланг', reply_markup=date_buttons(from_user_id, date_list=DATA_FOR_DATE[from_user_id]))

# Userlar bilan ishlash qismi tugadi


# -------------------------------End Vazifa qo'sish----------------------------------------------------------------


# -------------------------------Start Xisobotni ko'rish----------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == 'view_report')
def reaction_view_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        bot.send_message(chat_id, 'Вазифа санасини танланг', reply_markup=date_buttons_for_reports(from_user_id))


@bot.callback_query_handler(func=lambda call: 'view_down_report|' in call.data)
def reaction_view_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)


    try:
        from openpyxl import Workbook
        wb = Workbook()

        # grab the active worksheet
        ws = wb.active


        date_id = int(call.data.split("|")[-1])
        date = db.select_date_by_id_and_admin_id(date_id, from_user_id)[0]
        users = db.select_user_file_id_user_id_by_admin_id_and_date_id(from_user_id, date_id)
        if users:
            # print(users)
            d = {}
            ws.append(["Ф.И.Ш", "Телефон ракам", "Мажлис санаси", "Вазифа номи", "Бажариб болинган сана"])
            for user in users:
                user_id = user[0]
                user_file_id = user[1]
                file_id = user[2]

                task_name = db.select_file_name_by_id_and_user_telegram_id(file_id, from_user_id)[0]

                user_date = db.select_user_date_by_user_id_and_user_file_id(user_id, user_file_id)[0]
                full_name, phone_number = db.select_user_by_telegram_id(user_id)

                if d.get(user_date):
                    d[user_date].append(
                        [full_name, phone_number, date, task_name]
                    )
                else:
                    d[user_date] = [
                        [full_name, phone_number, date, task_name]
                    ]

            new_d = list(d.keys())
            new_d.sort(key=lambda x: datetime.strptime(x, '%d.%m.%Y'))

            for key in new_d:
                value = d[key]
                for user_info in value:
                    user_info.append(key)
                    ws.append(user_info)

                # ws.append([full_name, phone_number, date, task_name, user_date])
            # for user_date, value in d.items():
            #     for i in value:
            #         i.append(user_date)
            #         ws.append(i)

            wb.save(f"files/{date}.xlsx")
            d.clear()

            bot.send_message(chat_id, "Хисобот файл")
            with open(f'files/{date}.xlsx', mode='rb') as file:
                bot.send_document(chat_id, document=file, reply_markup=admin_panel_button(from_user_id))

            import os
            os.remove(f"files/{date}.xlsx")
        else:
            bot.send_message(chat_id, "Хисобот файл мавжуд емас", reply_markup=admin_panel_button(from_user_id))
    except:
        bot.send_message(chat_id, "Nimadir xato ketdi!", reply_markup=admin_panel_button(from_user_id))

    # bot.send_message(chat_id, 'Вазифа санасини танланг', reply_markup=date_buttons_for_reports(from_user_id))
    # bot.send_message(chat_id, "Асосий сахифа", reply_markup=admin_panel_button(from_user_id))



@bot.callback_query_handler(func=lambda call: call.data == 'next_page_report')
def reaction_next_page_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_report':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, 'Вазифа санасини танланг', reply_markup=date_buttons_for_reports(from_user_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'previous_page_report')
def reaction_previous_page_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_report':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, 'Вазифа санасини танланг', reply_markup=date_buttons_for_reports(from_user_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page_report')
def reaction_to_current_page_report(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_report':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")


def pagination(from_user_id, date_id, page=1):
    task_date = db.select_date_by_id(date_id)[0]
    limit = 1
    count = db.count_file_by_date_id(date_id)[0]
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    files = db.pagination_file_by_date_id(from_user_id, date_id, offset, limit)
    files.reverse()
    text = "Хисобот"
    markup = report_buttons1(date_id, max_page, page)
    if count > 0:
        for file_ids in files:
            if file_ids[0]:
                user_file_id = int(file_ids[0])
                user_id = int(file_ids[1])
                task_file_id = int(file_ids[2])

                user_name = db.select_user_by_telegram_id(user_id)[0]
                phone_number = db.select_user_by_telegram_id(user_id)[1]
                vazifa_name = db.select_file_name_by_id(task_file_id)[0]
                done_task_date = db.select_user_file_date(user_file_id)[0]

                text = (f"Ф.И.Ш: {user_name}\n"
                        f"Телефон раками: {phone_number}\n"
                        f"Мажлис санаси: {task_date}\n"
                        f"Вазифа номи: {vazifa_name}\n"
                        f"Бажариб болинган сана: {done_task_date}")

                markup = report_buttons1(date_id, max_page, page)

    else:
        text = "Бу санада хисоботлар мавжуд эмас.\nВазифа санасини танланг"
        markup = date_buttons_for_reports(from_user_id)

    return (text, markup)



@bot.callback_query_handler(func=lambda call: "view_report|" in call.data)
def reaction_to_view_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)

    text, markup = pagination(from_user_id, date_id)
    bot.send_message(chat_id, text, reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == 'admin_buttons')
def reaction_to_admin_buttons(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())


'''Vazifalarni chiqarish'''


@bot.callback_query_handler(func=lambda call: "next_rep|" in call.data)
def reaction_next_page_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_rep':
            page = int(keyboard.text)
    if page:
        page += 1
        text, markup = pagination(from_user_id, date_id, page)
        bot.send_message(chat_id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'previous_rep|' in call.data)
def reaction_previous_page_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_rep':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            text, markup = pagination(from_user_id, date_id, page)
            bot.send_message(chat_id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'current_rep')
def reaction_to_current_page_report(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_rep':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")



@bot.callback_query_handler(func=lambda call: "v_rep|" in call.data)
def reaction_to_view_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_file_id = int(call.data.split('|')[1])
    date_id = int(call.data.split('|')[2])
    bot.delete_message(chat_id, call.message.message_id)

    file = db.select_file_by_id(user_file_id)[0]
    user_id = db.select_file_by_id(user_file_id)[1]
    user_name, phone_number = db.select_user_by_telegram_id(user_id)
    bot.send_document(chat_id, document=file, caption=f"{user_name}\n{phone_number}",
                      reply_markup=admin_panel_button(from_user_id))

    # files = db.select_user_file_id_by_file_id_and_date_id(file_id, date_id)
    # for user_file_id in files:
    #     user_file_id = user_file_id[0]
    #     file = db.select_file_by_user_file_id(user_file_id)[0]
    #     bot.send_document(chat_id, document=file)
    # bot.send_message(chat_id, "Шу санадаги барча хисоботлар", reply_markup=admin_panel_button(from_user_id))


@bot.callback_query_handler(func=lambda call: "back_rep|" in call.data)
def reaction_to_back_rep(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'Вазифа санасини танланг', reply_markup=date_buttons_for_reports(from_user_id))


'''Vazifalarni chiqarish tugadi'''


# -------------------------------End Xisobotni ko'rish------------------------------------------------------------------


# -------------------------------Start Хисоботни юклаб олиш------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == 'download_report')
def reaction_to_download_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    try:
        from openpyxl import Workbook
        wb = Workbook()

        # grab the active worksheet
        ws = wb.active
        ws.append(["Ф.И.Ш", "Телефон ракам", "Мажлис санаси", "Вазифа номи", "Бажариб болинган сана"])

        user_files_id = db.select_user_file_id_by_admin_id(from_user_id)

        bot.send_message(chat_id, "Хисобот файл")
        user_files_id.reverse()
        d2 = {}
        for user_file_id in user_files_id:
            foydalanuvchi_file_id = int(user_file_id[0])
            task_file_id = int(user_file_id[1])
            date_id = int(user_file_id[2])
            user_id = int(user_file_id[3])

            user_name, phone_number = db.select_user_by_telegram_id(user_id)
            task_date = db.select_date_by_id(date_id)[0]
            task_name = db.select_file_name_by_id(task_file_id)[0]
            user_done_date = db.select_user_file_date(foydalanuvchi_file_id)[0]

            if d2.get(user_done_date):
                d2[user_done_date].append([user_name, phone_number, task_date, task_name])
            else:
                d2[user_done_date] = [
                    [user_name, phone_number, task_date, task_name]
                ]

            # ws.append([user_name, phone_number, task_date, task_name, user_done_date])

        keys = list(d2.keys())
        keys.sort(key=lambda x: datetime.strptime(x, '%d.%m.%Y'))
        for key in keys:
            value = d2[key]
            for user_date in value:
                user_date.append(key)
                ws.append(user_date)
        wb.save(f"files/{from_user_id}.xlsx")
        d2.clear()

        with open(f'files/{from_user_id}.xlsx', mode='rb') as file:
            bot.send_document(chat_id, document=file, reply_markup=admin_panel_button(from_user_id))

        import os
        os.remove(f"files/{from_user_id}.xlsx")

    except:
        pass


# -------------------------------End Хисоботни юклаб олиш--------------------------------------------------------------


# -------------------------------Start Вазифа санасини учириш----------------------------------------------------------


@bot.callback_query_handler(func=lambda call: call.data == 'del_date_task')
def reaction_to_del_date_task(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Фойдаланувчиларни танланг", reply_markup=users_for_edit_date_buttons(from_user_id))


@bot.callback_query_handler(func=lambda call: call.data == 'next_page_edit_date')
def reaction_next_page_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_edit_date':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, 'Фойдаланувчиларни танланг', reply_markup=users_for_edit_date_buttons(from_user_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'previous_page_edit_date')
def reaction_previous_page_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_edit_date':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, 'Фойдаланувчиларни танланг', reply_markup=users_for_edit_date_buttons(from_user_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page_edit_date')
def reaction_to_current_page_report(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_edit_date':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")


@bot.callback_query_handler(func=lambda call: "v_edit_user_date0|" in call.data)
def reaction_to_view_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    user_name = db.select_user_by_telegram_id(user_id)[0]
    bot.answer_callback_query(call.id, f"{user_name}")


@bot.callback_query_handler(func=lambda call: "edit_user_date|" in call.data)
def reaction_to_view_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)
    USERS_FOR_EDIT[from_user_id] = {
        user_id: []
    }
    bot.send_message(chat_id, "Учирмокчи болган санангизни танланг", reply_markup=date_buttons_for_edit(user_id))

"""Vazifa sanasini o'chirish"""

@bot.callback_query_handler(func=lambda call: "next_date_edit|" in call.data)
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_date_edit':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, "Учирмокчи болган санангизни танланг",
                         reply_markup=date_buttons_for_edit(user_id, page))


@bot.callback_query_handler(func=lambda call: 'previous_date_edit|' in call.data)
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_date_edit':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, "Учирмокчи болган санангизни танланг",
                             reply_markup=date_buttons_for_edit(user_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'current_date_edit')
def reaction_to_view_user(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_date_edit':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")



@bot.callback_query_handler(func=lambda call: "view_date_edit|" in call.data)
def reaction_to_view_user(call: CallbackQuery):
    date_id = call.data.split('|')[1]
    date = db.select_date_by_id(date_id)[0]
    bot.answer_callback_query(call.id, f"{date}")


@bot.callback_query_handler(func=lambda call: "minus_date_edit|" in call.data)
def reaction_to_minus_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    user_id = int(call.data.split('|')[2])
    USERS_FOR_EDIT[from_user_id][user_id].append(date_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_date_edit':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=date_buttons_for_edit(user_id, page, USERS_FOR_EDIT[from_user_id][user_id]))


@bot.callback_query_handler(func=lambda call: "plus_date_edit|" in call.data)
def reaction_to_plus_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    user_id = int(call.data.split('|')[2])
    USERS_FOR_EDIT[from_user_id][user_id].remove(date_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_date_edit':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=date_buttons_for_edit(user_id, page, USERS_FOR_EDIT[from_user_id][user_id]))


@bot.callback_query_handler(func=lambda call: 'cancel_for_date_edit|' in call.data)
def reaction_to_cancel_date_edit(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)
    try:
        del USERS_FOR_EDIT[from_user_id][user_id]
    except:
        pass
    bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())



@bot.callback_query_handler(func=lambda call: 'commit_del_for_date_edit|' in call.data)
def reaction_to_commit_del_for_date_edit(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    user_name = db.select_user_by_telegram_id(user_id)[0]
    bot.delete_message(chat_id, call.message.message_id)
    if from_user_id in ADMINS:
        dates = USERS_FOR_EDIT[from_user_id][user_id]
        for date_id in dates:
            db.delete_date_and_user(user_id, date_id)
        bot.send_message(chat_id, f"{user_name}га богланган сана ўчирилди", reply_markup=admin_commands_button())




@bot.callback_query_handler(func=lambda call: 'bekor_qilish|' in call.data)
def reaction_to_bekor_qilish(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    try:
        # del data_for_date[from_user_id]
        del DATA_FOR_DATE[from_user_id]
    except:
        pass
    bot.send_message(chat_id, "Вазифа бекор килинди", reply_markup=admin_panel_button(from_user_id))


"""Vazifa sanasini o'chirish tugadi"""


# -------------------------------End Вазифа санасини учириш------------------------------------------------------------


# -------------------------------Start Вазифани учириш------------------------------------------------------------

DATE_FOR_DEL_TASK = {}
@bot.callback_query_handler(func=lambda call: call.data == 'del_report')
def reaction_to_del_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    DATE_FOR_DEL_TASK[from_user_id] = {
        'tasks': []
    }
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Фойдаланувчиларни танланг", reply_markup=users_for_del_tasks_buttons(from_user_id))



@bot.callback_query_handler(func=lambda call: call.data == 'next1_del_task')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current1_del_task':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, "Вазифа учун сана танланг",
                         reply_markup=users_for_del_tasks_buttons(from_user_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'previous1_del_task')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current1_del_task':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, "Вазифа учун сана танланг",
                             reply_markup=users_for_del_tasks_buttons(from_user_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'current1_del_task')
def reaction_to_view_user(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current1_del_task':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")



@bot.callback_query_handler(func=lambda call: "view1_del_task|" in call.data)
def reaction_to_view_user(call: CallbackQuery):
    user_id = call.data.split('|')[1]
    user_name = db.select_user_by_telegram_id(user_id)[0]
    bot.answer_callback_query(call.id, f"{user_name}")


@bot.callback_query_handler(func=lambda call: call.data == 'cancel1_del_task')
def reaction_to_cancel_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    try:
        if DATE_FOR_DEL_TASK.get(from_user_id):
            del DATE_FOR_DEL_TASK[from_user_id]
    except:
        pass
    bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())


@bot.callback_query_handler(func=lambda call: "edit1_del_task|" in call.data)
def reaction_to_minus_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    DATE_FOR_DEL_TASK[from_user_id]['user_id'] = user_id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Учирмокчи болган вазифангизни санасини танланг",
                     reply_markup=date_buttons_for_del_tasks(user_id))


'''Sanalar bilan ishlash'''

@bot.callback_query_handler(func=lambda call: "next2_date_edit|" in call.data)
def reaction_next_page_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current2_date_edit':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, 'Фойдаланувчиларни танланг', reply_markup=date_buttons_for_del_tasks(user_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'previous2_date_edit')
def reaction_previous_page_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    user_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current2_date_edit':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, 'Фойдаланувчиларни танланг', reply_markup=date_buttons_for_del_tasks(user_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'cancel2_for_del_task')
def reaction_to_current_page_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Асосий сахифа", reply_markup=admin_panel_button(from_user_id))


@bot.callback_query_handler(func=lambda call: call.data == 'current2_date_edit')
def reaction_to_current_page_report(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current2_date_edit':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")


@bot.callback_query_handler(func=lambda call: "view2_date_edit|" in call.data)
def reaction_to_view_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id

    # date_id = int(call.data.split('|')[1])
    # user_name = db.select_user_by_telegram_id(user_id)[0]
    # bot.answer_callback_query(call.id, f"{user_name}")


@bot.callback_query_handler(func=lambda call: "minus2_date_edit|" in call.data)
def reaction_to_view_report(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    user_id = int(call.data.split('|')[2])
    bot.delete_message(chat_id, call.message.message_id)

    # DATE_FOR_DEL_TASK[from_user_id]['date_id'] = date_id
    #
    # USERS_FOR_EDIT[from_user_id] = {
    #     user_id: []
    # }

    bot.send_message(chat_id, "Учирмокчи болган вазифангизни  танланг",
                     reply_markup=task_buttons_for_del_tasks_(user_id, date_id))


"""Vazifa sanasini o'chirish"""


@bot.callback_query_handler(func=lambda call: "next3_task|" in call.data)
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    user_id = int(call.data.split('|')[2])
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current3_date_edit':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, "Учирмокчи болган вазифангизни  танланг",
                         reply_markup=task_buttons_for_del_tasks_(user_id, date_id, page, DATE_FOR_DEL_TASK[from_user_id]['tasks']))


@bot.callback_query_handler(func=lambda call: 'previous3_task|' in call.data)
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    user_id = int(call.data.split('|')[2])
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current3_date_edit':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, "Учирмокчи болган вазифангизни  танланг",
                             reply_markup=task_buttons_for_del_tasks_(user_id, date_id, page, DATE_FOR_DEL_TASK[from_user_id]['tasks']))


@bot.callback_query_handler(func=lambda call: call.data == 'current3_date_edit')
def reaction_to_view_user(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current3_date_edit':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")



@bot.callback_query_handler(func=lambda call: "view3_date_edit|" in call.data)
def reaction_to_view_user(call: CallbackQuery):
    file_id = call.data.split('|')[1]
    task_name = db.select_file_name_by_id(file_id)[0]
    bot.answer_callback_query(call.id, f"{task_name}")


@bot.callback_query_handler(func=lambda call: "minus3_task|" in call.data)
def reaction_to_minus_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    file_id = int(call.data.split('|')[1])
    date_id = int(call.data.split('|')[2])
    user_id = int(call.data.split('|')[3])

    DATE_FOR_DEL_TASK[from_user_id]['tasks'].append(file_id)

    # print(DATE_FOR_DEL_TASK)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current3_date_edit':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=task_buttons_for_del_tasks_(user_id, date_id, page, DATE_FOR_DEL_TASK[from_user_id]['tasks']))


@bot.callback_query_handler(func=lambda call: "plus3_task|" in call.data)
def reaction_to_minus_date(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    file_id = int(call.data.split('|')[1])
    date_id = int(call.data.split('|')[2])
    user_id = int(call.data.split('|')[3])
    # print(file_id, date_id, user_id)
    # print(DATE_FOR_DEL_TASK)

    if file_id in DATE_FOR_DEL_TASK[from_user_id]['tasks']:
        DATE_FOR_DEL_TASK[from_user_id]['tasks'].remove(file_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current3_date_edit':
            page = int(keyboard.text)
    if page:
        bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                      reply_markup=task_buttons_for_del_tasks_(user_id, date_id, page, DATE_FOR_DEL_TASK[from_user_id]['tasks']))



@bot.callback_query_handler(func=lambda call: call.data == 'cancel3_for_del_task')
def reaction_to_cancel_date_edit(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    try:
        del DATE_FOR_DEL_TASK[from_user_id]
    except:
        pass
    bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())


@bot.callback_query_handler(func=lambda call: 'delete3_task|' in call.data)
def reaction_to_cancel_date_edit(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    user_id = int(call.data.split('|')[2])

    bot.delete_message(chat_id, call.message.message_id)

    files_id = DATE_FOR_DEL_TASK[from_user_id]['tasks']
    for file_id in files_id:
        db.delete_file_by_user_id_and_date_id(file_id, user_id, date_id)
    try:
        del DATE_FOR_DEL_TASK[from_user_id]
    except:
        pass
    bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())

'''Sanalar bilan ishlash tugadi'''


# -------------------------------End Вазифани учириш------------------------------------------------------------


@bot.callback_query_handler(func=lambda call: call.data == "nazad1")
def nazad1(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Админ Буйруқлари", reply_markup=admin_commands_button())



@bot.callback_query_handler(func=lambda call: call.data == "nazad2")
def nazad1(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    try:
        if data.get(from_user_id):
            del data[from_user_id]
    except:
        pass
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Парол сакланмади", reply_markup=admin_commands_button())