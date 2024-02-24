'''CALLBACKLARNI ILADIGAN HANDLERLAR'''
from telebot.types import CallbackQuery, Message
from data.loader import bot, db
from keyboards.inline import date_buttons_for_user, view_file_buttons
from keyboards.default import cancel_send, admin_panel_button
from config import ADMINS
import datetime

sana_malumoti = []

@bot.callback_query_handler(func=lambda call: call.data == 'next_page_sana')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_sana':
            page = int(keyboard.text)
    if page:
        page += 1
        bot.send_message(chat_id, "Мажлислар санаси",
                         reply_markup=date_buttons_for_user(from_user_id, page, sana_malumoti))


@bot.callback_query_handler(func=lambda call: call.data == 'previous_page_sana')
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_sana':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1
            bot.send_message(chat_id, "Мажлислар санаси",
                             reply_markup=date_buttons_for_user(from_user_id, page, sana_malumoti))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page_sana')
def reaction_to_view_user(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'current_page_sana':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")



@bot.callback_query_handler(func=lambda call: "sanani_korish|" in call.data)
def reaction_to_view_user(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    date_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)
    try:
        file_ids = db.select_file_id_by_user_id_and_date_id(from_user_id, date_id)
        if file_ids:
            # file_id = db.select_file_id_by_user_id_and_date_id(from_user_id, date_id)[0][0]
            # for file_id in file_ids:
            # file_name = db.select_file_name_by_id(file_id)[0]

            file_name, markup = view_file_buttons(from_user_id, date_id)
            if file_name:
                text = file_name
            else:
                text = "Бу санада бошка вазифа мавжуд эмас"

            bot.send_message(chat_id, text, reply_markup=markup)
        else:
            bot.send_message(chat_id, "Бу санага хозирча вазифа кушилмаган", reply_markup=date_buttons_for_user(from_user_id))
    except:
        print('except ishladi')
        pass
        # bot.send_message(chat_id, "Сизга хозирча вазифа кушилмаган",
        #                  reply_markup=date_buttons_for_user(from_user_id))


@bot.callback_query_handler(func=lambda call: "file_name|" in call.data)
def reaction_to_file_name(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    print('test2')
    file_id = int(call.data.split('|')[1])
    file_name = db.select_file_name_by_id(file_id)[0]
    file = db.select_file_by_id(file_id)[0]

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_document(chat_id, document=file, caption=f"{file_name}")

file_data = {}
@bot.callback_query_handler(func=lambda call: "bajarildi|" in call.data)
def reaction_to_bajarildi(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    old_file_id = int(call.data.split('|')[1])
    bot.delete_message(chat_id, call.message.message_id)
    # file_data[from_user_id] = {
    #         'old_file_id': file_id
    #     }
    date = datetime.datetime.now().strftime('%d.%m.%Y')
    db.insert_user_file_on_users_files(from_user_id, 'yes', date)

    user_file_ids = db.select_id(from_user_id, 'yes', date)
    count_user_file_ids = len(user_file_ids)
    if count_user_file_ids > 1:
        user_file_id = user_file_ids[-1][0]
    else:
        user_file_id = user_file_ids[0][0]

    # user_file_id = db.select_user_file_from_user_files('yes')[0]
    # old_file_id = file_data[from_user_id]['old_file_id']
    db.insert_user_file_id(user_file_id, old_file_id, from_user_id)
    bot.send_message(chat_id, "Ҳисобот қабул қилинди")
    bot.send_message(chat_id, "Тақдим этилган маълумотлар учун рахмат", reply_markup=admin_panel_button(from_user_id))
    # msg = bot.send_message(chat_id, "Файлни йуборинг", reply_markup=cancel_send())
    # bot.register_next_step_handler(msg, get_user_file)


# def get_user_file(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     if message.text:
#         if message.text == "Бекор қилиш":
#             bot.send_message(chat_id, "Асосий сахифа", reply_markup=admin_panel_button(from_user_id))
#         else:
#             msg = bot.send_message(chat_id, "Файлни йуборилмади қайта йуборинг", reply_markup=cancel_send())
#             bot.register_next_step_handler(msg, get_user_file)
#     elif message.document:
#         file = message.document.file_id
        # db.insert_user_file_on_users_files(from_user_id, file)
        # file_id = db.select_user_file_from_user_files(file)[0]
        # old_file_id = file_data[from_user_id]['old_file_id']
        # db.insert_user_file_id(file_id, old_file_id, from_user_id)
        # bot.send_message(chat_id, "Ҳисобот қабул қилинди")
        # bot.send_message(chat_id, "Тақдим этилган маълумотлар учун рахмат", reply_markup=admin_panel_button(from_user_id))
    # else:
    #     msg = bot.send_message(chat_id, "Файлни йуборилмади қайта йуборинг", reply_markup=cancel_send())
    #     bot.register_next_step_handler(msg, get_user_file)


@bot.callback_query_handler(func=lambda call: "bajarilgan|" in call.data)
def reaction_to_bajarilgan(call: CallbackQuery):
    bot.answer_callback_query(call.id, text="Бажарилган")


@bot.callback_query_handler(func=lambda call: "keyingi_sahifa|" in call.data)
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    date_id = int(call.data.split('|')[1])
    file_id = int(call.data.split('|')[2])
    file_name = db.select_file_name_by_id(file_id)[0]

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'shu_sana':
            page = int(keyboard.text)
    if page:
        page += 1

        file_name, markup = view_file_buttons(from_user_id, date_id, page)
        if file_name:
            text = file_name
        else:
            text = "Бу санада бошка вазифа мавжуд эмас"

        bot.send_message(chat_id, text, reply_markup=markup)

        # bot.send_message(chat_id, f"{file_name}",
        #                  reply_markup=view_file_buttons(from_user_id, date_id, page))


@bot.callback_query_handler(func=lambda call: "oldingi_sahifa|" in call.data)
def reaction_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)

    date_id = int(call.data.split('|')[1])
    file_id = int(call.data.split('|')[2])
    file_name = db.select_file_name_by_id(file_id)[0]

    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'shu_sana':
            page = int(keyboard.text)
    if page:
        if page > 1:
            page -= 1

            file_name, markup = view_file_buttons(from_user_id, date_id, page)
            if file_name:
                text = file_name
            else:
                text = "Бу санада бошка вазифа мавжуд эмас"

            bot.send_message(chat_id, text, reply_markup=markup)

            # bot.send_message(chat_id, f"{file_name}",
            #                  reply_markup=view_file_buttons(from_user_id, date_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'shu_sana')
def reaction_to_view_user(call: CallbackQuery):
    keyboards = call.message.reply_markup.keyboard[-2]
    page = None
    for keyboard in keyboards:
        if keyboard.callback_data == 'shu_sana':
            page = int(keyboard.text)
    if page:
        bot.answer_callback_query(call.id, f"{page} - сахифа!")
