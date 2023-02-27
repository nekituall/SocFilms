
import mysql.connector
import time
from mysql.connector import Error


#для БД
config = {
    "user": "user",
    "password": "1ngodwetrust",
    "host": "127.0.0.1",
    "database" : "socfilms_db"
}


def create_conn(config):
    """create coonection using config"""
    try:
        conn = mysql.connector.connect(**config)
        conn.autocommit = True
        print("Connection succeed")
        return conn
    except Error as e:  #чтото с привелегиями dba??
        print(f"Connection failed due to {e}")


def deploy_db():
    """aux func to deploy DB onto MySQL"""
    conn = create_conn(config)
    cur = conn.cursor()
    try:
        with open("db//db_create.sql") as f:
            deploy_query = f.read()
        cur.execute(deploy_query)
        print(f"DB deployed at {time.asctime()}")  # в лог
    except Error as e:
        print(f"DB not deployed at {time.asctime()} with {e}")


def close_db(conn):
    """closing conncetion with database"""
    conn.close()


def create_user(person):
    """add new user
    person - сущность пользвоателя в виде кортежа
    """
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("""INSERT INTO users (`name`,`surname`,`nickname`,
  `email`,`country`) VALUES (%s,%s,%s,%s,%s)""", person)
    close_db(conn)
    print("Added")

def ask_friend(values):
    """ask for new friend
    values кортеж = (отправитель запроса, получатель запроса)
    """
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("""INSERT INTO friends (`main_user`,`friend_user`) VALUES (%s,%s)""", values)
    close_db(conn)
    print("ASKed for friend")


def confirm_friend(values):
    """confirm new friend"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("""UPDATE friends SET `valid`=1 WHERE (`main_user`,`friend_user`)=(%s,%s)""", values)
    close_db(conn)
    print("ASKed for friend")


def delete_friend():
    """delete a friend"""
    pass


def add_film():
    """Add favourite film
    1) если нету в общем списке films, тогда заполняются данные о фильме и автоматом добавляются данные в таблицу favorite_films
    2) иначе, добавляется запись в таблицу favorite_films
    """
    pass


def delete_film():
    """Delete favourite film
    удаляется запись из таблицы favorite_films
    """
    pass





if __name__ == "__main__":
    create_user(("Julia", "Kut", "Kutashek", "kutashek@ya.ru", "Russia"))