
import mysql.connector
import time
from mysql.connector import OperationalError

#для БД
config = {
    "user": "user",
    "password": "1ngodwetrust",
    "host": "127.0.0.1"
}

with open("db//db_create.sql") as f:
    deploy_query = f.read()
    # print(deploy_query)

def create_db(config):
    """create database using config"""
    try:
        con = mysql.connector.connect(**config)
        cur = con.cursor()
        print("Connection succeed")
        cur.execute(deploy_query)
        print(f"DB deployed at {time.asctime()}")  # в лог
        return con, cur
    except OperationalError as e:  #чтото с привелегиями..создается только если dba
        print(f"con failed due to {e}")


def close_db(con,cur):
    """closing conncetion with database"""
    con.close()
    cur.close()


def create_user(con,cur,values):
    """add new user"""
    cur.execute("""INSERT INTO users VALUES (?)""", (values,))
    cur.commit()


def create_friend():
    pass


def delete_friend():
    pass


def add_film():
    pass


def delete_film():
    pass

create_db(config)