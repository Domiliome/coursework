import sqlite3

# получить список писателей  по шаблону
def get_writers_data(table, name, sign, date, country):
    conn = sqlite3.connect('writers.db')
    cur = conn.cursor()
    get_data_query = f"SELECT * FROM {table} " \
                     f"WHERE full_name LIKE ('%{name}%') AND " \
                     f"year_of_birth {sign}= {date} AND " \
                     f"country LIKE ('%{country}%');"
    cur.execute(get_data_query)
    records = cur.fetchall()
    return records

# получить список произведений  по шаблону
def get_works_data(table, name="", sign=">", date=0, genre=""):
    conn = sqlite3.connect('writers.db')
    cur = conn.cursor()
    get_data_query = f"SELECT * FROM {table} " \
                     f"JOIN genres ON {table}.id_genre = genres.id_genre " \
                     f"WHERE {table}.name LIKE ('%{name}%') AND " \
                     f"{table}.year_of_writing {sign}= {date} AND " \
                     f"genres.name LIKE ('%{genre}%');"
    cur.execute(get_data_query)
    records = cur.fetchall()
    return records

# изменить пароль пользователя в базе данных
def change_pass(user, new_password):
    conn = sqlite3.connect('writers.db')
    cur = conn.cursor()
    change_pass_query = f"UPDATE users " \
                        f"SET password = '{new_password}' " \
                        f"WHERE login IS '{user[3]}';"
    cur.execute(change_pass_query)
    conn.commit()
    conn.close()

# получить данные писателя
def get_user_data(id):
    conn = sqlite3.connect('writers.db')
    cur = conn.cursor()
    get_data_query = f"SELECT * FROM users " \
                     f"WHERE id_user = {id};"
    cur.execute(get_data_query)
    records = cur.fetchall()
    records = [x for l in records for x in l]
    print(records)
    return records

# получить список пользователей
def get_users():
    conn = sqlite3.connect('writers.db')
    cur = conn.cursor()
    get_data_query = f"SELECT * FROM users;"
    cur.execute(get_data_query)
    records = cur.fetchall()
    return records

# получить произведения автора
def get_author_works(id):
    conn = sqlite3.connect('writers.db')
    cur = conn.cursor()
    get_data_query = f"SELECT name FROM works WHERE id_writer = {id};"
    cur.execute(get_data_query)
    records = cur.fetchall()
    return records

# добавить произведение в базу данных
def add_work_record(data):
    conn = sqlite3.connect('writers.db')
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO works (id_writer, id_genre, name, year_of_writing) VALUES (?, ?, ?, ?)""",
        (author_id(data[0]), genre_id(data[1]), data[2], data[3]))
    conn.commit()
    conn.close()

# добавить писателя в базу данных
def add_author_record(data):
    conn = sqlite3.connect('writers.db')
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO writers (full_name, year_of_birth, country, biography, portrait) VALUES (?, ?, ?, ?, ?)""",
        (data[0], data[1], data[2],
         convert_to_binary_data(f"biographies/{data[3]}.txt"),
         convert_to_binary_data(f"portraits/{data[4]}.png")))
    conn.commit()
    conn.close()

# получить идентификатор автора
def author_id(full_name):
    result = simple_executor(query=f"SELECT id_writer FROM writers WHERE full_name = '{full_name}';")
    return result

# получить имя автора
def author_name(id):
    result = simple_executor(query=f"SELECT full_name FROM writers WHERE id_writer = '{id}';")
    return result

# получить идентификатор жанра
def genre_id(name):
    result = simple_executor(query=f"SELECT id_genre FROM genres WHERE name = '{name}';")
    return result

# получить название жанра
def genre_name(id):
    result = simple_executor(query=f"SELECT name FROM genres WHERE id_genre = '{id}';")
    return result

# выполнение простых запросов в базе данных
def simple_executor(query):
    conn = sqlite3.connect('writers.db')
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]

# преобразовать файл к бинарному виду
def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


class WriterDB:
    def __init__(self):
        pass

    def convert_to_binary_data(self, filename):
        # Преобразование данных в двоичный формат
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    def update_record(self):
        conn = sqlite3.connect('writers.db')
        cur = conn.cursor()
        cur.execute("UPDATE writers SET full_name = 'Фёдор Михайлович Достоевский' "
                    "WHERE id_writer = 2;")
        conn.commit()
        conn.close()

    def add_genre_record(self):
        conn = sqlite3.connect('writers.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO genres (name) VALUES ('Комедия');")
        conn.commit()
        conn.close()

    def add_user(self):
        conn = sqlite3.connect('writers.db')
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO users (privelegy,full_name, login, password, data_of_delete_pass, status, portrait) VALUES (?, ?, ?, ?, ?, ?,?)""",
            ("user", "Высоцкий Леонид Григорьевич", "vysockiy", '123456', "10", "active",
             self.convert_to_binary_data("portraits/london.txt")))
        conn.commit()
        conn.close()

    def del_record(self):
        conn = sqlite3.connect('writers.db')
        cur = conn.cursor()
        cur.execute("""DELETE FROM works WHERE id_work = 10;""")
        conn.commit()
        conn.close()

    def del_table(self):
        self.get_id("""""")

    def create_db(self):
        conn = sqlite3.connect('writers.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS writers(
                        id_writer INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        full_name TEXT NOT NULL,
                        year_of_birth INTEGER NOT NULL,
                        country TEXT NOT NULL,
                        biography BLOB NOT NULL,
                        portrait BLOB);
                        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS genres(
                                id_genre INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                name TEXT);
                                """)

        cur.execute("""CREATE TABLE IF NOT EXISTS work(
                        id_work INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        id_writer INTEGER NOT NULL,
                        id_genre INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        year_of_writing INTEGER NOT NULL,
                        FOREIGN KEY (id_writer) REFERENCES writers (id_writer),
                        FOREIGN KEY (id_genre) REFERENCES genres (id_genre));
                        """)
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                                id_user INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                privelegy TEXT NOT NULL,
                                                full_name TEXT NOT NULL,
                                                login text NOT NULL,
                                                password TEXT NOT NULL,
                                                data_of_delete_pass TEXT,
                                                status TEXT NOT NULL,
                                                portrait BLOB);
                                                """)
        conn.commit()
        conn.close()


WriterDB()
