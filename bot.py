'''
BOTNI ISHGA TUSHIRISH
'''
from middlewares import SimpleMiddleware
from data.loader import bot, db

import handlers

# db.drop_users_files()
# db.drop_table_ids()
# db.drop_table_user_and_date()
db.create_table_password()
db.create_table_users()
db.create_table_date()
db.create_table_user_and_date()
db.create_table_for_files()
db.create_table_file_id_and_date_id_and_user_id()
db.create_table_users_files()


bot.setup_middleware(SimpleMiddleware(1)) # bu botga qayta qayta yozmaslik uchun limit(sekundda) kiritiladi

if __name__ == '__main__':
    import time
    # bot.infinity_polling()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(2)

            