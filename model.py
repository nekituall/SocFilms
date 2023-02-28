
import mysql.connector
import time
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


def deploy_db():
    """вспомогательная функция по развертке DB onto MySQL
        будут нужны права ДБА"""
    conn = create_conn(config_deploy)
    cur = conn.cursor()
    try:
        with open("db//db_create.sql") as f:
            deploy_query = f.read()
        cur.execute(deploy_query)
        print(f"DB deployed at {time.asctime()}")  # в лог
    except Error as e:
        print(f"DB not deployed at {time.asctime()} with {e}")


def close_db(conn):
    """закрывает подключение к DB"""
    try:
        conn.close()
    except Error as e:
        print(f"Conn not closed due to {e}")



def create_user(person):            #ПАРОЛЬ добавить!!!!!
    """добавить нового пользователя
    person - сущность пользвоателя в виде кортежа
    """
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("INSERT INTO users (`name`,`surname`,`nickname`, `email`,`country`) VALUES (%s,%s,%s,%s,%s)")
    cur.execute(query, person)
    close_db(conn)
    print("Added")

def ask_friend(values):
    """запросить дружбу
    values кортеж = (отправитель запроса, получатель запроса)
    """
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("INSERT INTO friends (`main_user`,`friend_user`) VALUES (%s,%s)")
    cur.execute(query, values)
    close_db(conn)
    print("ASKed for friend")


def confirm_friend(values):
    """одобрить дружбу"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("UPDATE friends SET `valid`=1 WHERE (`main_user`,`friend_user`, 'status')=(%s,%s, 'confirmed')")
    cur.execute(query, values)
    close_db(conn)
    print("Confirmed for friend")


def reject_friend(values):
    """отклонить дружбу"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("UPDATE friends SET `valid`=1 WHERE (`main_user`,`friend_user`, 'status')=(%s,%s, 'rejected')")
    cur.execute(query, values)
    close_db(conn)
    print("Confirmed for friend")

def delete_friend(values):
    """Удалить друга
    передать в values кортеж кто удаляет и кого удаляет"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("DELETE FROM friends WHERE (`main_user`,`friend_user`)=(%s,%s)")
    cur.execute(query, values)
    close_db(conn)
    print("Deleted friend")
    pass
# ROW_COUNT() для тестов


def search_film(name):
    """ищем фильм в базе данных, если нету то по АПИ"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("""SELECT filmname, year FROM films WHERE filmname=%s""", name)
    res = cur.fetchall()
    if res == 0:
        #запрос к АПИ
        data = search_api(name)
        return data
    else:
        close_db(conn)
        return cur.fetchall()


def add_film(value):
    """Добавить любимый фильм
    1) если нету в общем списке films, тогда заполняются данные о фильме и автоматом добавляются данные в таблицу favorite_films
    2) иначе, добавляется запись в таблицу favorite_films
    """
    conn = create_conn(config)
    cur = conn.cursor()
    query = """INSERT INTO films (`main_user`,`friend_user`) VALUES (%s,%s)"""
    cur.execute(query, value)
    close_db(conn)

    pass


def delete_film():
    """Удалить любимый фильм
    удаляется запись из таблицы favorite_films
    """
    pass





if __name__ == "__main__":
    create_user(("Julia", "Kut", "Kutashek", "kutashek@ya.ru", "Russia"))   #работает