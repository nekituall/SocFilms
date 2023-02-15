
import mysql.connector
from mysql.connector import OperationalError


config = {
    "user": "user",
    "password": "passwd",
    "host": "localhost",
    "database": "db"
}


def create_db(config):
    """create database using config"""
    try:
        con = mysql.connector.connect(**config)
        cur = con.cursor()
        print("Connection succeed")
        return con, cur
    except OperationalError as e:
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

