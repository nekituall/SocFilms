
import mysql.connector
import time
from mysql.connector import Error

#для БД
config = {
    "user": "user",
    "password": "1ngodwetrust",
    "host": "127.0.0.1"
}


def create_conn(config):
    """create coonection using config"""
    try:
        conn = mysql.connector.connect(**config)
        # conn = sqlite3.connect("test.db")
        conn.autocommit = True
        print("Connection succeed")
        return conn
    except Error as e:  #чтото с привелегиями dba??
        print(f"Connection failed due to {e}")


def deploy_db():
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
    """ask for new friend"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("""INSERT INTO friends (`main_user`,`friend_user`,`valid`) 
    VALUES (%s,%s,0)""", (values,))
    close_db(conn)
    print("ASKed for friend")


def confirm_friend(values):
    """confirm new friend"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("""UPDATE friends SET `valid`=1 WHERE (`main_user`,`friend_user`)=(%s,%s)""", (values,))
    close_db(conn)
    print("ASKed for friend")


def delete_friend():
    """delete a friend"""
    pass


def add_film():
    pass


def delete_film():
    pass
