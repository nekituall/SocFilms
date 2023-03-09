import time

import mysql.connector
from mysql.connector import Error, IntegrityError

from view import search_api

#для развертки БД
config_deploy = {
    "user": "user",
    "password": "1ngodwetrust",
    "host": "127.0.0.1"
}

config = {
    "user": "user",
    "password": "1ngodwetrust",
    "host": "127.0.0.1",
    "database" : "socfilms_db"
}


def create_conn(config):
    """создать подключение к БД"""
    try:
        conn = mysql.connector.connect(**config)
        print("Connection succeed")
        return conn
    except Error as e:  #чтото с привелегиями dba??
        print(f"Connection failed due to {e}")


def deploy_db(config_deploy):
    """вспомогательная функция по развертке DB onto MySQL
        будут нужны права ДБА"""
    try:
        conn = mysql.connector.connect(**config_deploy)
        cur = conn.cursor()
        try:
            with open("db//db_create_final.sql") as f:
                deploy_query = f.read()
            cur.execute(deploy_query)
            print(f"DB deployed at {time.asctime()}")  # в лог
        except Error as e:
            print(f"DB not deployed at {time.asctime()} with {e}")
        close_db(conn)
    except Error as e:
        print(f"Connection failed due to {e}")


def close_db(conn):
    """закрывает подключение к DB"""
    try:
        conn.close()
    except Error as e:
        print(f"Conn not closed due to {e}")


def create_user(person):
    """добавить нового пользователя
    person - сущность пользвоателя в виде кортежа
    """
    try:
        conn = create_conn(config)
        cur = conn.cursor()
        query = ("INSERT INTO users (name, surname, nickname, passw, email, country) VALUES (%s,%s,%s,%s,%s,%s);")
        cur.execute(query, person)
        conn.commit()
        close_db(conn)
        print("User added")
    except mysql.connector.errors.IntegrityError as e:
        print(f"{e} occured")


def search_user(name):
    """поиск пользователя по никнейму"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("SELECT name, surname, nickname, country FROM users WHERE nickname=%s;", name)
    user_data = cur.fetchall()
    if len(user_data) != 0:
        close_db(conn)
        print(user_data)
        return user_data
    else:
        print("No such user")
        return "No such user"


def login_user(name, passw):
    """Попытка залогиниться"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("SELECT idusers FROM users WHERE (nickname, passw)=(%s,%s);", (name,passw))
    user_login = cur.fetchall()
    if len(user_login) != 0:
        close_db(conn)
        return user_login
    else:
        return None


def show_friends(user_id, status):
    """Показать всех друзей"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("""SELECT us.nickname, us.country, fr.status FROM users as us JOIN friends as fr 
    ON us.idusers=fr.friend_user WHERE fr.main_user=%s AND fr.status=%s;""", (user_id, status))
    friends = cur.fetchall()
    if len(friends) != 0:
        close_db(conn)
        print(friends)
        return friends
    else:
        close_db(conn)
        print("No friends yet..")
        return "No friends yet.."

def ask_friend(values):
    """запросить дружбу
    values кортеж = (отправитель запроса, получатель запроса)
    """
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("INSERT INTO friends (main_user, friend_user) VALUES (%s,%s);")
    cur.execute(query, values)
    conn.commit()
    close_db(conn)
    print("ASKed for friend")


def confirm_friend(values):
    """одобрить дружбу"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("UPDATE friends SET status='confirmed' WHERE (main_user, friend_user)=(%s,%s);")
    cur.execute(query, values)
    conn.commit()
    close_db(conn)
    print("Confirmed for friend")


def reject_friend(values):
    """отклонить дружбу"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("UPDATE friends SET status='rejected' WHERE (main_user, friend_user)=(%s,%s);")
    cur.execute(query, values)
    conn.commit()
    close_db(conn)
    print("Rejected friend")

def delete_friend(values):
    """Удалить друга
    передать в values кортеж кто удаляет и кого удаляет"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("DELETE FROM friends WHERE (main_user, friend_user)=(%s,%s);")
    cur.execute(query, values)
    conn.commit()
    close_db(conn)
    print("Deleted friend")
# ROW_COUNT() для тестов


def search_film(name:tuple) -> list:
    """ищем фильм в базе данных, если нету то по АПИ"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("SELECT filmname, year FROM films WHERE filmname=%s;", name)
    res = cur.fetchall()
    print(res)
    if len(res) == 0:
        print("api")
        #запрос к АПИ
        data = search_api(name[0])
        print(data)
        return data
    else:
        print("я в бд")
        close_db(conn)
        return res


def add_film(value: tuple):
    """Добавить  фильм
    при добавлении фильма проверяются таблицы жанров и стран, чтобы не было дубликатов
    """
    conn = create_conn(config)
    cur = conn.cursor(buffered=True)
    query_add_film = "INSERT INTO films (filmname, year) VALUES (%s,%s);"
    cur.execute(query_add_film, value[:2])
    film_id = cur.lastrowid
    def add_country(film_id):
        for country in value[3]:
            query = "SELECT idcountries FROM countries WHERE countryname=%s;"
            cur.execute(query, (country,))
            row = cur.fetchone()
            if row != None:
                countryid = row[0]
            else:
                query_country = "INSERT INTO countries (countryname) VALUES (%s);"   #добавить страну в таблицу
                cur.execute(query_country, (country,))
                cur.execute("SELECT LAST_INSERT_ID();")
                countryid = cur.fetchone()[0]
            cur.execute("INSERT INTO countryfilms (id_film, id_country) VALUES (%s,%s);", (film_id, countryid))

    def add_genre(film_id):
        for genre in value[2]:
            cur.execute("SELECT idgenres FROM genres WHERE genre=%s;", (genre,))
            row = cur.fetchone()
            if row != None:
                genreid = row[0]
            else:
                query_genre = "INSERT INTO genres (genre) VALUES (%s);"   #добавить жанр в таблицу
                cur.execute(query_genre, (genre,))
                genreid = cur.lastrowid
            cur.execute("INSERT INTO genrefilms (id_films, id_genre) VALUES (%s, %s);", (film_id, genreid))
    add_country(film_id)      # работает
    add_genre(film_id)        # работает
    conn.commit()
    close_db(conn)
    print("Film added to film list")


def add_favourite(value: tuple):
    """добавить любимый фильм
    работает только после добавления в общую таблицу фильмов"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = "INSERT INTO favouritefilms (user_id, film_id, add_date, rating, comments) VALUES (%s,%s,%s,%s,%s);"
    cur.execute(query, value)
    close_db(conn)
    print("Added to favourites")


def delete_favourite(value: tuple):
    """Удалить любимый фильм
    удаляется запись из таблицы favorite_films"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = "DELETE FROM favouritefilms WHERE (user_id, film_id)=(%s,%s);"
    cur.execute(query, value)
    close_db(conn)
    print("Deleted from favourites")


a = ("Julia",   "Kut",      "Kutashek", "passw1", "kutashek@ya.ru", "Russia")
b = ('Nikita',	'Pavlov',	'niknik', 'passw',	'kolbase@mail.ru',	'Bangladesh')
c = ('Vasya',	'Ganin',	'pikNick',  'passw',	'pikNick@mail.ru',	'Bangladesh')
d = ('Luci',	'Liu',	'Lucinda23',  'passw',	'Lucinda23@fail.ru',	'Canada')
film1 = ('Титаник', 1997, ['мелодрама', 'история', 'триллер', 'драма'], ['США', 'Мексика'])
film2 = ('Титаник', 2012, ['документальный', 'драма'], ['Россия'])
film3 = ('Бэтмен: Начало', 2005, ['боевик', 'фантастика', 'приключения', 'драма'], ['США', 'Великобритания'])

if __name__ == "__main__":
    # deploy_db(config_deploy)      # работает
    # create_user(d)                # работает
    # search_user(("Kut",))       # работает
    # ask_friend((3, 1))          # работает
    show_friends(3, "confirmed")
    # confirm_friend((3,2))       # работает
    # reject_friend((3, 2))       # работает
    # delete_friend((3, 4))       # работает
    # search_film(("Титаник",))      # работает
    # add_film(film3)               # работает
    # add_favourite((12, 2, "2023-04-11", 3, "для семейного просмотра"))       #работает , если дата-строчка
    # delete_favourite((12, 1))       # работает
    pass