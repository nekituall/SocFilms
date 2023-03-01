import time

import mysql.connector
from mysql.connector import Error

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
        conn.autocommit = True
        print("Connection succeed")
        return conn
    except Error as e:  #чтото с привелегиями dba??
        print(f"Connection failed due to {e}")


def deploy_db(config_deploy):
    """вспомогательная функция по развертке DB onto MySQL
        будут нужны права ДБА"""
    try:
        conn = mysql.connector.connect(**config_deploy)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            with open("db//db_create.sql") as f:
                deploy_query = f.read()
            cur.execute(deploy_query)
            print(f"DB deployed at {time.asctime()}")  # в лог
        except Error as e:
            print(f"DB not deployed at {time.asctime()} with {e}")
    except Error as e:
        print(f"Connection failed due to {e}")
    close_db(conn)


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
        query = ("INSERT INTO users (name, surname, nickname, passw, email, country) VALUES (%s,%s,%s,%s,%s,%s)")
        cur.execute(query, person)
        close_db(conn)
        print("User added")
    except mysql.connector.errors.IntegrityError as e:
        print(f"{e} occured")


def ask_friend(values):
    """запросить дружбу
    values кортеж = (отправитель запроса, получатель запроса)
    """
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("INSERT INTO friends (main_user, friend_user) VALUES (%s,%s)")
    cur.execute(query, values)
    close_db(conn)
    print("ASKed for friend")


def confirm_friend(values):
    """одобрить дружбу"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("UPDATE friends SET status='confirmed' WHERE (main_user, friend_user)=(%s,%s)")
    cur.execute(query, values)
    close_db(conn)
    print("Confirmed for friend")


def reject_friend(values):
    """отклонить дружбу"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("UPDATE friends SET status='rejected' WHERE (`main_user`,`friend_user`)=(%s,%s)")
    cur.execute(query, values)
    close_db(conn)
    print("Confirmed for friend")

def delete_friend(values):
    """Удалить друга
    передать в values кортеж кто удаляет и кого удаляет"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("DELETE FROM friends WHERE (main_user, friend_user)=(%s,%s)")
    cur.execute(query, values)
    close_db(conn)
    print("Deleted friend")
# ROW_COUNT() для тестов


def search_film(name:tuple) -> list:
    """ищем фильм в базе данных, если нету то по АПИ"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("SELECT filmname, year FROM films WHERE filmname=%s", name)
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
    1) если нету в общем списке films, тогда заполняются данные о фильме и автоматом добавляются данные в таблицу favorite_films
    2) иначе, добавляется запись в таблицу favorite_films
    """
    conn = create_conn(config)
    cur = conn.cursor()
    query = "INSERT INTO films (filmname, year, genre, country) VALUES (%s,%s,%s,%s)"
    cur.execute(query, value)
    close_db(conn)
    print("Thanks! Added to film list")


def add_favourite(value: tuple):
    """добавить любимый фильм
    работает только после добавления в общую таблицу фильмов"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = "INSERT INTO favouritefilms (user_id, film_id, add_date, rating, comments) VALUES (%s,%s,%s,%s,%s)"
    cur.execute(query, value)
    close_db(conn)
    print("Added to favourites")


def delete_favourite(value: tuple):
    """Удалить любимый фильм
    удаляется запись из таблицы favorite_films"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = "DELETE FROM favouritefilms WHERE (user_id, film_id)=(%s,%s)"
    cur.execute(query, value)
    close_db(conn)
    print("Deleted from favourites")


a = ("Julia",   "Kut",      "Kutashek", "passw1", "kutashek@ya.ru", "Russia")
b = ('Nikita',	'Pavlov',	'niknik', 'passw',	'kolbase@mail.ru',	'Bangladesh')
c = ('Vasya',	'Ganin',	'pikNick',  'passw',	'pikNick@mail.ru',	'Bangladesh')
d = ('Luci',	'Liu',	'Lucinda23',  'passw',	'Lucinda23@fail.ru',	'Canada')
film1 = ('Бэтмен: Начало', 2005, 'боевик, фантастика, приключения, драма', 'США, Великобритания')
film2 = ('Титаник', 1997, 'мелодрама, история, триллер, драма', 'США, Мексика')


if __name__ == "__main__":
    # deploy_db(config_deploy)      # работает
    # create_user(a)                # работает
    # ask_friend((12, 15))          # работает
    # confirm_friend((12,15))       # работает
    # reject_friend((12, 15))       # работает
    # delete_friend((12, 15))       # работает
    # search_film(("Титаник",))      # работает
    # add_film(film2)     #работает НО записывает в поле несколько стран и жанров!!!!
    # add_favourite((12, 2, "2023-04-11", 3, "для семейного просмотра"))       #работает , если дата-строчка
    # delete_favourite((12, 1))       # работает
    pass