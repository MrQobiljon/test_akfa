import sqlite3



class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # ------------------------------------------------------------------------------------------------------------------
    # password tablitsasi

    def create_table_password(self):
        sql = '''CREATE TABLE IF NOT EXISTS passwords(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT,
            logic VARCHAR(1)
        )'''
        self.execute(sql, commit=True)

    def select_password(self):
        sql = '''SELECT password, logic FROM passwords LIMIT 1'''
        return self.execute(sql, fetchone=True)

    def insert_password(self, password, logic):
        sql = '''INSERT INTO passwords(password, logic) VALUES (?, ?)'''
        self.execute(sql, parameters=(password, logic), commit=True)

    def update_password(self, new_password, old_password):
        sql = '''UPDATE passwords SET password = ? WHERE password = ?'''
        self.execute(sql, parameters=(new_password, old_password), commit=True)

    def off_on_password(self, logic, password):
        sql = '''UPDATE passwords SET logic = ? WHERE password = ?'''
        self.execute(sql, parameters=(logic, password), commit=True)

    def delete_password(self, password):
        sql = '''DELETE FROM passwords WHERE password = ?'''
        self.execute(sql, parameters=(password,), commit=True)

    # ------------------------------------------------------------------------------------------------------------------
    # users tablitsasi

    def create_table_users(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id INTEGER PRIMARY KEY,
            full_name VARCHAR(255),
            phone_number VARCHAR(18),
            logic VARCHAR(1)
        )'''
        self.execute(sql, commit=True)

    def insert_user_telegram_id(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES (?) ON CONFLICT DO NOTHING'''
        self.execute(sql, parameters=(telegram_id,), commit=True)

    def select_user_by_telegram_id(self, telegram_id):
        sql = '''SELECT full_name, phone_number FROM users WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def select_logic_from_user(self, telegram_id):
        sql = '''SELECT logic FROM users WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def update_logic_on_users(self, logic, telegram_id):
        sql = '''UPDATE users SET logic = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(logic, telegram_id), commit=True)

    def save_user(self, full_name, phone_number, logic, telegram_id):
        sql = '''UPDATE users SET full_name = ?, phone_number = ?, logic = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(full_name, phone_number, logic, telegram_id), commit=True)

    def select_all_users(self):
        sql = '''SELECT full_name, telegram_id FROM users'''
        return self.execute(sql, fetchall=True)

    def delete_user(self, telegram_id):
        sql = '''DELETE FROM users WHERE telegram_id = ?'''
        self.execute(sql, parameters=(telegram_id,), commit=True)

    def select_all_users_by_pagination(self, offset, limit):
        sql = '''SELECT telegram_id, full_name FROM users
        LIMIT ?, ?'''
        return self.execute(sql, parameters=(offset, limit), fetchall=True)

    def count_users(self):
        sql = '''SELECT count(telegram_id) FROM users'''
        return self.execute(sql, fetchone=True)[0]

    # ------------------------------------------------------------------------------------------------------------------
    # dates tablitsasi

    def create_table_date(self):
        sql = '''CREATE TABLE IF NOT EXISTS dates(
            id INTEGER PRiMARY KEY AUTOINCREMENT,
            date VARCHAR(11),
            admin_id INTEGER
        )'''
        self.execute(sql, commit=True)

    def insert_date(self, date, admin_id):
        sql = '''INSERT INTO dates(date, admin_id) VALUES (?, ?)'''
        self.execute(sql, parameters=(date, admin_id), commit=True)

    # def select_date_id(self, date):
    #     sql = '''SELECT id FROM dates WHERE date = ?'''
    #     return self.execute(sql, parameters=(date,), fetchone=True)

    def select_date_id(self, date, admin_id):
        sql = '''SELECT id FROM dates WHERE date = ? AND admin_id = ?'''
        return self.execute(sql, parameters=(date, admin_id), fetchone=True)

    def count_dates(self, admin_id):
        sql = '''SELECT count(id) FROM dates WHERE admin_id = ?'''
        return self.execute(sql, parameters=(admin_id,), fetchone=True)[0]

    def select_dates_by_pagination(self, admin_id, offset, limit):
        sql = '''SELECT id, date FROM dates WHERE admin_id = ?
        LIMIT ?, ?'''
        return self.execute(sql, parameters=(admin_id, offset, limit), fetchall=True)

    def select_date_by_id(self, date_id):
        sql = '''SELECT date FROM dates WHERE id = ?'''
        return self.execute(sql, parameters=(date_id,), fetchone=True)

    def select_date_by_id_and_admin_id(self, date_id, admin_id):
        sql = """SELECT date FROM dates WHERE id = ? AND admin_id = ?"""
        return self.execute(sql, parameters=(date_id, admin_id), fetchone=True)

    # ------------------------------------------------------------------------------------------------------------------
    # user_and_date tablitsasi

    def create_table_user_and_date(self):
        sql = '''CREATE TABLE IF NOT EXISTS user_and_date(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_id INTEGER,
        user_id INTEGER,
        admin_id INTEGER
        )'''
        self.execute(sql, commit=True)

    def drop_table_user_and_date(self):
        sql = '''DROP TABLE IF EXISTS user_and_date'''
        self.execute(sql, commit=True)

    def insert_date_and_user(self, date_id, user_id, admin_id):
        sql = '''INSERT INTO user_and_date(date_id, user_id, admin_id) VALUES (?, ?, ?)'''
        self.execute(sql, parameters=(date_id, user_id, admin_id), commit=True)

    def select_all_user_id_by_date_id(self, date_id, admin_id):
        sql = '''SELECT user_id FROM user_and_date WHERE date_id = ? AND admin_id = ?'''
        return self.execute(sql, parameters=(date_id, admin_id), fetchall=True)

    def select_dates_for_user(self, user_id):
        sql = '''SELECT date_id FROM user_and_date WHERE user_id = ?'''
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def count_user_and_date_by_user_id(self, user_id):
        sql = '''SELECT count(date_id) FROM user_and_date WHERE user_id = ?'''
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    def pagination_user_an_date_by_user_id(self, user_id, offset, limit):
        sql = '''SELECT date_id FROM user_and_date WHERE user_id = ? 
        LIMIT ?, ?'''
        return self.execute(sql, parameters=(user_id, offset, limit), fetchall=True)

    # def pagination_user_an_date_by_user_id_for_admin(self, admin_id, offset, limit):
    #     sql = '''SELECT date_id FROM user_and_date WHERE admin_id = ?
    #     LIMIT ?, ?'''
    #     return self.execute(sql, parameters=(admin_id, offset, limit), fetchall=True)

    def pagination_user_an_date_by_user_id_for_admin(self, admin_id, offset, limit):
        sql = '''SELECT DISTINCT date_id FROM user_and_date WHERE admin_id = ? 
        LIMIT ?, ?'''
        return self.execute(sql, parameters=(admin_id, offset, limit), fetchall=True)

    def delete_date_and_user(self, user_id, date_id):
        sql = '''DELETE FROM user_and_date WHERE user_id = ? AND date_id = ?'''
        self.execute(sql, parameters=(user_id, date_id), commit=True)

    def count_users_dates(self, admin_id):
        sql = '''SELECT count(date_id) FROM user_and_date WHERE admin_id = ?'''
        return self.execute(sql, parameters=(admin_id,), fetchone=True)

    def select_all_users_dates_by_pagination(self, admin_id, offset, limit):
        sql = '''SELECT DISTINCT user_id FROM user_and_date WHERE admin_id = ?
        LIMIT ?, ?'''
        return self.execute(sql, parameters=(admin_id, offset, limit), fetchall=True)

    # ------------------------------------------------------------------------------------------------------------------
    # files tablitsasi

    def create_table_for_files(self):
        sql = '''CREATE TABLE IF NOT EXISTS files(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            file TEXT,
            user_telegram_id INTEGER
        )'''
        self.execute(sql, commit=True)

    def insert_file(self, task_name, file_id, admin_id):
        sql = '''INSERT INTO files(task_name, file, user_telegram_id) VALUES (?, ?, ?)'''
        self.execute(sql, parameters=(task_name, file_id, admin_id), commit=True)

    def select_id_by_file_text_id(self, file_text_id):
        sql = '''SELECT id FROM files WHERE file = ?'''
        return self.execute(sql, parameters=(file_text_id,), fetchone=True)

    def select_file_name_by_id(self, file_id):
        sql = '''SELECT task_name FROM files WHERE id = ?'''
        return self.execute(sql, parameters=(file_id,), fetchone=True)

    def select_file_by_id(self, file_id):
        sql = '''SELECT file, user_telegram_id FROM files WHERE id = ?'''
        return self.execute(sql, parameters=(file_id,), fetchone=True)

    def select_file_name_by_id_and_user_telegram_id(self, file_id, admin_id):
        sql = '''SELECT task_name FROM files WHERE id = ? AND user_telegram_id = ?'''
        return self.execute(sql, parameters=(file_id, admin_id), fetchone=True)



    # ------------------------------------------------------------------------------------------------------------------
    # ids tablitsasi

    def create_table_file_id_and_date_id_and_user_id(self):
        '''User file id sini o'rniga user_file tablitsasida bajardi va bajarmadi degan so'zlar qo'laniladi.'''
        sql = '''CREATE TABLE IF NOT EXISTS ids(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER,
            date_id INTEGER,
            user_id INTEGER,
            user_file_id INTEGER,
            admin_id INTEGER,
            del VARCHAR(4)
        )'''
        self.execute(sql, commit=True)

    def drop_table_ids(self):
        sql = '''DROP TABLE IF EXISTS ids'''
        self.execute(sql, commit=True)

    def update_ids_for_user(self, confirmation_del, user_id, admin_id):
        sql = '''UPDATE ids SET del = ? WHERE user_id = ? AND admin_id = ?'''
        self.execute(sql, parameters=(confirmation_del, user_id, admin_id), commit=True)

    def insert_file_id_date_id_user_id(self, file_id, date_id, user_id, admin_id):
        sql = '''INSERT INTO ids(file_id, date_id, user_id, admin_id) VALUES (?, ?, ?, ?)'''
        self.execute(sql, parameters=(file_id, date_id, user_id, admin_id), commit=True)

    def select_file_id_by_user_id_and_date_id(self, user_telegram_id, date_id):
        sql = '''SELECT file_id FROM ids WHERE user_id = ? and date_id = ?'''
        return self.execute(sql, parameters=(user_telegram_id, date_id), fetchall=True)

    def insert_user_file_id(self, user_file_id, file_id, user_telegram_id):
        sql = '''UPDATE ids SET user_file_id = ? WHERE file_id = ? and user_id = ?'''
        self.execute(sql, parameters=(user_file_id, file_id, user_telegram_id), commit=True)

    def count_file_by_date_id(self, date_id):
        sql = '''SELECT count(user_file_id) FROM ids WHERE date_id= ? AND user_file_id IS NOT NULL'''
        return self.execute(sql, parameters=(date_id,), fetchone=True)

    def pagination_file_by_date_id(self, admin_id, date_id, offset, limit):
        sql = '''SELECT user_file_id, user_id, file_id FROM ids WHERE admin_id = ? AND date_id = ? AND user_file_id IS NOT NULL
        ORDER BY user_file_id DESC
        LIMIT ?, ?'''
        return self.execute(sql, parameters=(admin_id, date_id, offset, limit), fetchall=True)

    def select_file_id_by_user_id_and_date_id_pagination(self, user_telegram_id, date_id, offset, limit):
        sql = '''SELECT file_id FROM ids WHERE user_id = ? and date_id = ? LIMIT ?, ?'''
        return self.execute(sql, parameters=(user_telegram_id, date_id, offset, limit), fetchall=True)

    def select_user_file_id_by_file_id_and_date_id(self, file_id, date_id):
        sql = '''SELECT user_file_id FROM ids WHERE file_id = ? AND date_id = ?'''
        return self.execute(sql, parameters=(file_id, date_id), fetchall=True)

    def count_user_id(self, admin_id):
        sql = '''SELECT count(DISTINCT user_id) FROM ids WHERE admin_id = ?'''
        return self.execute(sql, parameters=(admin_id,), fetchone=True)

    def select_user_file_id_by_file_id_date_id_user_id(self, file_id, date_id, user_id):
        sql = '''SELECT user_file_id FROM ids WHERE file_id = ? AND date_id = ? AND user_id = ?'''
        return self.execute(sql, parameters=(file_id, date_id, user_id), fetchone=True)

    def pagination_user_id_by_admin_id(self, admin_id, offset, limit):
        sql = '''SELECT DISTINCT user_id FROM ids WHERE admin_id = ? AND del IS NULL
        LIMIT ?, ?'''
        return self.execute(sql, parameters=(admin_id, offset, limit), fetchall=True)

    def count_files_by_user_id_and_date_id(self, user_id, date_id):
        sql = '''SELECT count(file_id) FROM ids WHERE user_id = ? AND date_id = ?'''
        return self.execute(sql, parameters=(user_id, date_id), fetchone=True)

    def pagination_file_id_by_user_id_and_date_id(self, user_id, date_id, offset, limit):
        sql = '''SELECT DISTINCT file_id FROM ids WHERE user_id = ? AND date_id = ?
        LIMIT ?, ?'''
        return self.execute(sql, parameters=(user_id, date_id, offset, limit), fetchall=True)

    def delete_file_by_user_id_and_date_id(self, file_id, user_id, date_id):
        sql = '''DELETE FROM ids WHERE file_id = ? AND user_id = ? AND date_id = ?'''
        self.execute(sql, parameters=(file_id, user_id, date_id), commit=True)

    def select_user_file_id_by_admin_id(self, admin_id):
        sql = '''SELECT user_file_id, file_id, date_id, user_id FROM ids WHERE admin_id = ? AND 
        user_file_id IS NOT NULL'''
        return self.execute(sql, parameters=(admin_id,), fetchall=True)

    def select_user_file_id_user_id_by_admin_id_and_date_id(self, admin_id, date_id):
        sql = """SELECT user_id, user_file_id, file_id FROM ids WHERE admin_id = ? AND date_id = ? AND user_file_id IS NOT NULL"""
        return self.execute(sql, parameters=(admin_id, date_id), fetchall=True)


    # ------------------------------------------------------------------------------------------------------------------
    # users_files tablitsasi

    def create_table_users_files(self):
        sql = '''CREATE TABLE IF NOT EXISTS users_files(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_telegram_id INTEGER,
            file TEXT,
            date TEXT
        )'''
        self.execute(sql, commit=True)

    def insert_user_file_on_users_files(self, user_telegram_id, file, date):
        sql = '''INSERT INTO users_files(user_telegram_id, file, date) VALUES (?, ?, ?)'''
        self.execute(sql, parameters=(user_telegram_id, file, date), commit=True)

    def select_id(self, user_telegram_id, file, date):
        sql = '''SELECT id FROM users_files WHERE user_telegram_id = ? AND file = ? AND date = ?'''
        return self.execute(sql, parameters=(user_telegram_id, file, date), fetchall=True)

    def select_user_file_from_user_files(self, file, user_telegram_id):
        sql = '''SELECT id FROM users_files WHERE file = ? AND user_telegram_id = ?'''
        return self.execute(sql, parameters=(file, user_telegram_id), fetchone=True)

    def select_file_by_user_file_id(self, user_file_id):
        sql = '''SELECT file FROM users_files WHERE id = ?'''
        return self.execute(sql, parameters=(user_file_id,), fetchone=True)

    def download_all_user_files(self):
        sql = '''SELECT file FROM users_files'''
        return self.execute(sql, fetchall=True)

    def select_user_id_by_user_file_id(self, user_file_id):
        sql = '''SELECT user_telegram_id FROM users_files WHERE id = ?'''
        return self.execute(sql, parameters=(user_file_id,), fetchone=True)

    def select_user_file_by_id(self, file_id):
        sql = '''SELECT file FROM users_files WHERE id = ?'''
        return self.execute(sql, parameters=(file_id,), fetchone=True)

    def drop_users_files(self):
        sql = '''DROP TABLE IF EXISTS users_files'''
        self.execute(sql, commit=True)

    def select_user_file_date(self, file_id):
        sql = '''SELECT date FROM users_files WHERE id = ?'''
        return self.execute(sql, parameters=(file_id,), fetchone=True)

    def select_user_date_by_user_id_and_user_file_id(self, user_id, file_id):
        sql = """SELECT date FROM users_files WHERE user_telegram_id = ? AND id = ?"""
        return self.execute(sql, parameters=(user_id, file_id), fetchone=True)




    # ------------------------------------------------------------------------------
    # test uchun

    def insert_user(self, telegram_id, full_name, phone_number, logic):
        sql = '''INSERT INTO users(telegram_id, full_name, phone_number, logic) VALUES (?, ?, ?, ?)
        ON CONFLICT DO NOTHING'''
        self.execute(sql, parameters=(telegram_id, full_name, phone_number, logic), commit=True)



