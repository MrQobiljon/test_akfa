'''
SIZ BU YERDA INLINE KNOPKALAR YARATA OLASIZ
'''
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.loader import db


def admin_commands_button():
    markup = InlineKeyboardMarkup(row_width=1)

    if db.select_password():
        text = "Паролни ўзгартириш"
        call = "change_password"
    else:
        text = "Паролни қўшиш"
        call = "add_password"

    btn1 = InlineKeyboardButton(text, callback_data=call)
    btn2 = InlineKeyboardButton('Вазифа санасини қўшиш', callback_data='add_date_task')
    btn3 = InlineKeyboardButton("Вазифа кўшиш", callback_data="add_task")
    btn4 = InlineKeyboardButton('Хисоботни кўриш', callback_data="view_report")
    btn5 = InlineKeyboardButton("Вазифа санасини учириш", callback_data="del_date_task")
    btn6 = InlineKeyboardButton('Фойдаланувчиларни рўйхатини кўриш', callback_data="view_list_users")
    btn7 = InlineKeyboardButton('Хисоботни юклаб олиш', callback_data="download_report")
    btn8 = InlineKeyboardButton("Вазифаларни учириш", callback_data="del_report")
    main_menu = InlineKeyboardButton("Асосий сахифа", callback_data="main_menu")

    markup.add(btn1)

    if db.select_password():
        btn1_2 = InlineKeyboardButton("Паролни ўчириш/ёқиш", callback_data="off_on_password")
        markup.add(btn1_2)

    markup.add(btn2, btn3, btn4, btn5, btn6, btn7, btn8, main_menu)
    return markup


def save_password_button():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("Паролни сақлаш", callback_data="save_password")
    back = InlineKeyboardButton("Ортга⬅️", callback_data="nazad2")
    markup.add(btn, back)
    return markup


def delete_password_buttons():
    markup = InlineKeyboardMarkup(row_width=1)
    if int(db.select_password()[1]) == 1:
        text = "Паролни вақтинчалик ўчириш"
        call = "temporarily_disable_the_password"
    else:
        text = "Паролни ёқиш"
        call = "enable_password"
    btn1 = InlineKeyboardButton(text, callback_data=call)
    btn2 = InlineKeyboardButton('Паролни бутунлай ўчириш', callback_data="delete_password_permanently")
    btn3 = InlineKeyboardButton("Ортга⬅️", callback_data="nazad1")
    markup.add(btn1, btn2, btn3)
    return markup


def all_users_buttons(page=1, user_list=[]):
    markup = InlineKeyboardMarkup(row_width=2)

    limit = 6
    count = db.count_users()
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    users = db.select_all_users_by_pagination(offset, limit)

    for user in users:
        btn1 = InlineKeyboardButton(f"{user[1]}", callback_data=f"view_user|{user[0]}")
        if user[0] in user_list:
            btn2 = InlineKeyboardButton('✔️', callback_data=f"s_user|{user[0]}")
        else:
            btn2 = InlineKeyboardButton('🗑', callback_data=f"s_user_for_del|{user[0]}")
        markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous_page")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_page")
    next = InlineKeyboardButton("⏭", callback_data=f"next_page")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Бекор қилиш", callback_data="cancel")
    clear = InlineKeyboardButton("Ўчириш", callback_data=f"confirmation_del_users")
    markup.add(back, clear)
    return markup




def users_for_date_buttons(page=1, user_list=[]):
    markup = InlineKeyboardMarkup(row_width=2)

    limit = 6
    count = db.count_users()
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    users = db.select_all_users_by_pagination(offset, limit)

    for user in users:
        btn1 = InlineKeyboardButton(f"{user[1]}", callback_data=f"v_user_for_date|{user[0]}")
        if user[0] in user_list:
            btn2 = InlineKeyboardButton('➕', callback_data=f"plus_user_date|{user[0]}")
        else:
            btn2 = InlineKeyboardButton('➖', callback_data=f"minus_user_d_del|{user[0]}")
        markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous_page_for_date")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_page_for_date")
    next = InlineKeyboardButton("⏭", callback_data=f"next_page_for_date")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Бекор қилиш", callback_data="cancel")
    clear = InlineKeyboardButton("Сақлаш", callback_data=f"save_users_for_date")
    markup.add(back, clear)
    return markup


def date_buttons(admin_id, page=1, date_list={}):
    markup = InlineKeyboardMarkup(row_width=2)

    limit = 6
    count = db.count_dates(admin_id)
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    # dates = db.select_dates_by_pagination(admin_id, offset, limit)
    dates = db.pagination_user_an_date_by_user_id_for_admin(admin_id, offset, limit)
    keys = list(date_list.keys())
    for date in dates:
        date_id = date[0]
        date_name = db.select_date_by_id(date_id)[0]
        btn1 = InlineKeyboardButton(f"{date_name}", callback_data=f"view_date|{date[0]}")
        if date[0] in keys:
            btn2 = InlineKeyboardButton('➕', callback_data=f"plus_date|{date[0]}")
        else:
            btn2 = InlineKeyboardButton('➖', callback_data=f"minus_date|{date[0]}")
        markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous_date")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_page_date")
    next = InlineKeyboardButton("⏭", callback_data=f"next_date")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Бекор қилиш", callback_data=f"cancel_date")
    send_file = InlineKeyboardButton("Файлни йубориш", callback_data=f"commit_send_file")
    markup.add(back, send_file)
    return markup


def users_buttons_for_tasks(date_id, admin_id, page=1, user_list=[]):
    users = {}
    markup = InlineKeyboardMarkup(row_width=2)

    user_id_list = db.select_all_user_id_by_date_id(date_id, admin_id)

    for user_id in user_id_list:
        user = db.select_user_by_telegram_id(user_id[0])[0]
        users[user_id[0]] = user

    limit = 6
    count = len(users)
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    users_id = list(users.keys())[offset:][:limit]
    for user_id in users_id:
        user = users[user_id]
        btn1 = InlineKeyboardButton(f"{user}", callback_data=f"user_for_task|{user_id}")
        if user_id in user_list:
            btn2 = InlineKeyboardButton('➕', callback_data=f"plus_user_task|{user_id}|{date_id}")
        else:
            btn2 = InlineKeyboardButton('➖', callback_data=f"minus_user_task|{user_id}|{date_id}")
        markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous_page_for_task|{date_id}")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_page_for_task")
    next = InlineKeyboardButton("⏭", callback_data=f"next_page_for_task|{date_id}")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Ортга", callback_data="back_to_date")
    send_file = InlineKeyboardButton("Файлни йубориш", callback_data=f"commit_send_file")
    markup.add(back, send_file)
    return markup


def confirmation_send_document():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Бекор қилиш", callback_data=f"bekor_qilish|")
    btn2 = InlineKeyboardButton("Вазифа юбориш", callback_data=f"vazifa_yuborish|")
    markup.add(btn1, btn2)
    return markup


def report_buttons1(date_id, max_page, page=1):
    markup = InlineKeyboardMarkup(row_width=1)

    back = InlineKeyboardButton("⏮", callback_data=f"previous_rep|{date_id}")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_rep")
    next = InlineKeyboardButton("⏭", callback_data=f"next_rep|{date_id}")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Ортга қайтиш", callback_data=f"back_rep|{date_id}")
    markup.add(back)
    return markup


def users_for_edit_date_buttons(admin_id, page=1, user_list=[]):
    markup = InlineKeyboardMarkup(row_width=2)

    limit = 6
    count = db.count_users_dates(admin_id)[0]
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    users = db.select_all_users_dates_by_pagination(admin_id, offset, limit)

    for user in users:
        user_id = user[0]
        user_name = db.select_user_by_telegram_id(user_id)[0]
        btn1 = InlineKeyboardButton(f"{user_name}", callback_data=f"v_edit_user_date0|{user_id}")
        # if user[0] in user_list:
        #     btn2 = InlineKeyboardButton('➕', callback_data=f"plus_e_user_date|{user[0]}")
        # else:
        btn2 = InlineKeyboardButton('➖', callback_data=f"edit_user_date|{user_id}")
        markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous_page_edit_date")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_page_edit_date")
    next = InlineKeyboardButton("⏭", callback_data=f"next_page_edit_date")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Бекор қилиш", callback_data="cancel")
    # clear = InlineKeyboardButton("Сақлаш", callback_data=f"save_users_for_date")
    markup.add(back)
    return markup



def date_buttons_for_edit(user_id, page=1, user_list=[]):
    markup = InlineKeyboardMarkup(row_width=2)

    limit = 6
    count = db.count_user_and_date_by_user_id(user_id)[0]
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    dates = db.pagination_user_an_date_by_user_id(user_id, offset, limit)
    for date_id in dates:
        date_id = date_id[0]
        date = db.select_date_by_id(date_id)[0]
        btn1 = InlineKeyboardButton(f"{date}", callback_data=f"view_date_edit|{date_id}")
        if date_id in user_list:
            btn2 = InlineKeyboardButton('➕', callback_data=f"plus_date_edit|{date_id}|{user_id}")
        else:
            btn2 = InlineKeyboardButton('➖', callback_data=f"minus_date_edit|{date_id}|{user_id}")
        markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous_date_edit|{user_id}")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_date_edit")
    next = InlineKeyboardButton("⏭", callback_data=f"next_date_edit|{user_id}")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Бекор қилиш", callback_data=f"cancel_for_date_edit|{user_id}")
    send_file = InlineKeyboardButton("Ўчириш", callback_data=f"commit_del_for_date_edit|{user_id}")
    markup.add(back, send_file)
    return markup



def users_for_del_tasks_buttons(admin_id, page=1, user_list=[]):
    markup = InlineKeyboardMarkup(row_width=2)

    limit = 6
    count = db.count_user_id(admin_id)[0]
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    users = db.pagination_user_id_by_admin_id(admin_id, offset, limit)

    for user in users:
        user_id = user[0]
        try:
            user_name = db.select_user_by_telegram_id(user_id)[0]
        except:
            user_name = None
        if user_name:
            btn1 = InlineKeyboardButton(f"{user_name}", callback_data=f"view1_del_task|{user_id}")
            # if user[0] in user_list:
            #     btn2 = InlineKeyboardButton('➕', callback_data=f"plus_e_user_date|{user[0]}")
            # else:
            btn2 = InlineKeyboardButton('➖', callback_data=f"edit1_del_task|{user_id}")
            markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous1_del_task")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current1_del_task")
    next = InlineKeyboardButton("⏭", callback_data=f"next1_del_task")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Бекор қилиш", callback_data="cancel1_del_task")
    # clear = InlineKeyboardButton("Сақлаш", callback_data=f"save_users_for_date")
    markup.add(back)
    return markup



def date_buttons_for_del_tasks(user_id, page=1, user_list=[]):
    markup = InlineKeyboardMarkup(row_width=2)

    limit = 6
    count = db.count_user_and_date_by_user_id(user_id)[0]
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    dates = db.pagination_user_an_date_by_user_id(user_id, offset, limit)
    for date_id in dates:
        date_id = date_id[0]
        date = db.select_date_by_id(date_id)[0]
        btn1 = InlineKeyboardButton(f"{date}", callback_data=f"view2_date_edit|{date_id}")
        # if date_id in user_list:
        #     btn2 = InlineKeyboardButton('➕', callback_data=f"plus_date_edit|{date_id}|{user_id}")
        # else:
        btn2 = InlineKeyboardButton('➖', callback_data=f"minus2_date_edit|{date_id}|{user_id}")
        markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous2_date_edit|{user_id}")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current2_date_edit")
    next = InlineKeyboardButton("⏭", callback_data=f"next2_date_edit|{user_id}")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Бекор қилиш", callback_data=f"cancel2_for_del_task")
    # send_file = InlineKeyboardButton("Ўчириш", callback_data=f"commit_del_for_date_edit|{user_id}")
    markup.add(back)
    return markup




def task_buttons_for_del_tasks_(user_id, date_id, page=1, tasks_list=[]):
    markup = InlineKeyboardMarkup(row_width=2)

    limit = 6
    count = db.count_files_by_user_id_and_date_id(user_id, date_id)[0]

    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    files = db.pagination_file_id_by_user_id_and_date_id(user_id, date_id, offset, limit)

    for file_id in files:
        file_id = file_id[0]
        file_name = db.select_file_name_by_id(file_id)[0]
        btn1 = InlineKeyboardButton(f"{file_name}", callback_data=f"view3_date_edit|{file_id}")
        if file_id in tasks_list:
            btn2 = InlineKeyboardButton('➕', callback_data=f"plus3_task|{file_id}|{date_id}|{user_id}")
        else:
            btn2 = InlineKeyboardButton('➖', callback_data=f"minus3_task|{file_id}|{date_id}|{user_id}")
        markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous3_task|{date_id}|{user_id}")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current3_date_edit")
    next = InlineKeyboardButton("⏭", callback_data=f"next3_task|{date_id}|{user_id}")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Бекор қилиш", callback_data=f"cancel3_for_del_task")
    back2 = InlineKeyboardButton("Ўчириш", callback_data=f"delete3_task|{date_id}|{user_id}")
    # send_file = InlineKeyboardButton("Ўчириш", callback_data=f"commit_del_for_date_edit|{user_id}")
    markup.add(back, back2)
    return markup




'''Foydalanuvchilarga ko'rinadigan qismi'''

def date_buttons_for_user(from_user_id, page=1, date_list=[]):
    markup = InlineKeyboardMarkup()
    dates = db.select_dates_for_user(from_user_id)
    dates_ids = []
    for date_id in dates:
        dates_ids.append(date_id[0])

    limit = 6
    count = len(dates_ids)
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    dates_ids_pagination = dates_ids[offset:][:limit]
    for date_id in dates_ids_pagination:
        date = db.select_date_by_id(date_id)[0]
        btn1 = InlineKeyboardButton(f"{date}", callback_data=f"sanani_korish|{date_id}")
        markup.add(btn1)

    back = InlineKeyboardButton("⏮", callback_data=f"previous_page_sana")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_page_sana")
    next = InlineKeyboardButton("⏭", callback_data=f"next_page_sana")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Ортга", callback_data="main_menu")
    markup.add(back)
    return markup


def view_file_buttons(user_telegram_id, date_id, page=1):
    markup = InlineKeyboardMarkup(row_width=1)

    file_ids = db.select_file_id_by_user_id_and_date_id(user_telegram_id, date_id)
    limit = 1
    count = len(file_ids)
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1

    file_ids = db.select_file_id_by_user_id_and_date_id_pagination(user_telegram_id, date_id, offset, limit)
    file_name = None
    if file_ids:
        for file_id in file_ids:
            file_name = db.select_file_name_by_id(file_id[0])
            btn = InlineKeyboardButton(f"Файл", callback_data=f"file_name|{file_id[0]}")
            check = db.select_user_file_id_by_file_id_date_id_user_id(file_id[0], date_id, user_telegram_id)[0]
            if check:
                btn2 = InlineKeyboardButton("Бажарилган", callback_data=f"bajarilgan|{file_id[0]}")
            else:
                btn2 = InlineKeyboardButton("Бажарилди", callback_data=f"bajarildi|{file_id[0]}")
            markup.add(btn, btn2)

            back = InlineKeyboardButton("⏮", callback_data=f"oldingi_sahifa|{date_id}|{file_id[0]}")
            current_page = InlineKeyboardButton(f"{page}", callback_data="shu_sana")
            next = InlineKeyboardButton("⏭", callback_data=f"keyingi_sahifa|{date_id}|{file_id[0]}")

            if 1 < page < max_page:
                markup.row(back, current_page, next)
            elif page == 1:
                markup.row(current_page, next)
            elif page == max_page:
                markup.row(back, current_page)

            back = InlineKeyboardButton("Ортга", callback_data="main_menu")
            markup.add(back)
    else:
        back = InlineKeyboardButton("Ортга", callback_data="main_menu")
        markup.add(back)

    return (file_name, markup)


def date_buttons_for_reports(admin_id, page=1):
    markup = InlineKeyboardMarkup()
    count = db.count_dates(admin_id)
    limit = 6
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1
    dates = db.select_dates_by_pagination(admin_id, offset, limit)
    for date in dates:
        btn1 = InlineKeyboardButton(f"{date[1]}", callback_data=f"view_report|{date[0]}")
        btn2 = InlineKeyboardButton(f"⬇️", callback_data=f"view_down_report|{date[0]}")
        markup.add(btn1, btn2)

    back = InlineKeyboardButton("⏮", callback_data=f"previous_page_report")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_page_report")
    next = InlineKeyboardButton("⏭", callback_data=f"next_page_report")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    back = InlineKeyboardButton("Ортга", callback_data="admin_buttons")
    markup.add(back)
    return markup