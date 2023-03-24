import time

import mysql.connector
from mysql.connector import Error

from api import search_api

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
    cur.execute("SELECT idusers, name, surname, nickname, country FROM users WHERE nickname=%s;", (name,))
    user_data = cur.fetchone()
    try:
        if len(user_data) != 0 and user_data is not None:
            close_db(conn)
            print(user_data)
            return user_data
        else:
            print("No such user")
            return "No such user"
    except:
        return None


def login_user(name, passw):
    """Попытка залогиниться"""
    conn = create_conn(config)
    cur = conn.cursor()
    cur.execute("SELECT idusers, nickname FROM users WHERE (nickname, passw)=(%s,%s);", (name,passw))
    user_login = cur.fetchone()
    print(user_login)
    if user_login is not None:
        close_db(conn)
        return user_login
    else:
        return None


def show_friends(user_id, status):
    """Показать всех друзей"""
    conn = create_conn(config)
    cur = conn.cursor()
    if  status == "asked":
        query = """SELECT us.idusers, us.name, us.surname, us.country, fr.status FROM users as us JOIN friends as fr 
    ON us.idusers=fr.main_user WHERE fr.friend_user=%s AND fr.status=%s;"""
        cur.execute(query, (user_id, status))
    if status == "confirmed":
        query= """SELECT us.idusers, us.name, us.surname, us.country, fr.status FROM users as us JOIN friends as fr 
    ON us.idusers=fr.main_user WHERE fr.friend_user=%s AND fr.status=%s UNION SELECT us.idusers, us.name, us.surname, us.country, fr.status FROM users as us JOIN friends as fr 
    ON us.idusers=fr.friend_user WHERE fr.main_user=%s  AND fr.status=%s;"""
        cur.execute(query, (user_id, status, user_id, status))
    # cur.execute("""SELECT us.name, us.surname, us.country, fr.status FROM users as us JOIN friends as fr
    # ON us.idusers=fr.main_user WHERE fr.friend_user=%s AND fr.status=%s;""", (user_id, status))
    # cur.execute("""SELECT us.name, us.surname, us.country, fr.status FROM users as us JOIN friends as fr
    #     ON us.idusers=fr.friend_user WHERE fr.main_user=%s AND fr.status=%s;""", (user_id, status))
    friends = cur.fetchall()
    if len(friends) != 0:
        close_db(conn)
        print(friends)
        return friends
    else:
        close_db(conn)
        print("No friends yet..")
        return None


def ask_friend(values):
    """запросить дружбу
    values кортеж = (отправитель запроса, получатель запроса)
    """
    conn = create_conn(config)
    cur = conn.cursor()
    # тут можно сделать проверку есть ли уже пользователь в друзьях перед запросом
    query = ("INSERT INTO friends (main_user, friend_user) VALUES (%s,%s);")
    cur.execute(query, values)
    conn.commit()
    close_db(conn)
    print("ASKed for friend")


def confirm_friend(values):
    """одобрить дружбу"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("UPDATE friends SET status='confirmed' WHERE ( friend_user, main_user)=(%s,%s);")
    cur.execute(query, values)
    conn.commit()
    close_db(conn)
    print("Confirmed for friend")


def reject_friend(values):
    """отклонить дружбу"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = ("UPDATE friends SET status='rejected' WHERE (friend_user, main_user)=(%s,%s);")
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


def search_film(name):
    """ищем фильм в базе данных, сравниваем с АПИ, если в базе нет, то добавляем его"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = """SELECT filmname, year, (SELECT group_concat(genre SEPARATOR ',') FROM genres g JOIN genrefilms gs ON g.idgenres=gs.id_genre WHERE gs.id_films = f.idfilms) AS genre,
    (SELECT group_concat(countryname SEPARATOR ',') FROM countries c JOIN countryfilms cs ON c.idcountries=cs.id_country WHERE cs.id_film = f.idfilms) AS countryname FROM films f JOIN genrefilms gs ON
        f.idfilms=gs.id_films JOIN genres g ON gs.id_genre=g.idgenres JOIN countryfilms cs ON f.idfilms=cs.id_film
        JOIN countries c ON cs.id_country=c.idcountries WHERE filmname LIKE %s GROUP BY f.idfilms;"""
    cur.execute(query, ("%" + name + "%",))
    db_data = cur.fetchall()
    # print(db_data)
    api_data = search_api(name)

    db_final = []
    for db in db_data:
        db = list(db)
        db[2] = db[2].split(",")
        db[3] = db[3].split(",")
        db_final.append(db)
    # print(db_final)

    if api_data is not None:
        api_final = [list(api) for api in api_data]
        # print(api_final)
        new_data = [x for x in api_final if x not in db_final]  # это данные, которых нету в базе
        for data in new_data:
            add_film(data)

    conn = create_conn(config)
    cur = conn.cursor()
    query_all = """SELECT idfilms, filmname, year, (SELECT group_concat(genre SEPARATOR ',') FROM genres g JOIN genrefilms gs ON g.idgenres=gs.id_genre WHERE gs.id_films = f.idfilms) AS genre,
        (SELECT group_concat(countryname SEPARATOR ',') FROM countries c JOIN countryfilms cs ON c.idcountries=cs.id_country WHERE cs.id_film = f.idfilms) AS countryname FROM films f JOIN genrefilms gs ON
            f.idfilms=gs.id_films JOIN genres g ON gs.id_genre=g.idgenres JOIN countryfilms cs ON f.idfilms=cs.id_film
            JOIN countries c ON cs.id_country=c.idcountries WHERE filmname LIKE %s GROUP BY f.idfilms;"""
    cur.execute(query_all, ("%" + name + "%",))
    all_data = cur.fetchall()
    print(all_data)
    return all_data

    #СТАРАЯ ВЕРСИЯ поиска по апи

    # conn = create_conn(config)
    # cur = conn.cursor()
    # # query = """SELECT filmname, year, genre, countryname FROM films f JOIN genrefilms gs ON
    # # f.idfilms=gs.id_films JOIN genres g ON gs.id_genre=g.idgenres JOIN countryfilms cs ON f.idfilms=cs.id_film
    # # JOIN countries c ON cs.id_country=c.idcountries WHERE filmname=%s GROUP BY f.idfilms;"""
    # # cur.execute(query, (name,))
    # # # чтобы вывести список похожий на апи с одним жанром и страной
    # cur.execute("SELECT filmname, year FROM films WHERE filmname=%s;", (name,))
    # res = cur.fetchall()
    # print(res)
    # # всегда через АПИ и наполнять базу
    # if len(res) == 0:
    #     print("api")
    #     #запрос к АПИ
    #     data = search_api(name)
    #     print(data)
    #     return data
    # else:
    #     print("я в бд")
    #     close_db(conn)
    #     return res


def add_film(value: list):
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


def show_favourites(value):
    """показать любимые фильмы"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = "SELECT films.filmname, films.year, fav.rating, fav.add_date, fav.comments from films JOIN favouritefilms as fav ON " \
            "films.idfilms=fav.film_id WHERE user_id=%s;"
    cur.execute(query, (value,))
    favourites = cur.fetchall()
    close_db(conn)
    print(favourites)
    return favourites


def add_favourites(value: tuple):
    """добавить любимый фильм
    работает только после добавления в общую таблицу фильмов"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = "INSERT INTO favouritefilms (user_id, film_id, add_date, rating, comments) VALUES (%s,%s,%s,%s,%s);"
    cur.execute(query, value)
    conn.commit()
    close_db(conn)
    print("Added to favourites")


def delete_favourites(value: tuple):
    """Удалить любимый фильм
    удаляется запись из таблицы favorite_films"""
    conn = create_conn(config)
    cur = conn.cursor()
    query = "DELETE FROM favouritefilms WHERE (user_id, film_id)=(%s,%s);"
    cur.execute(query, value)
    conn.commit()
    close_db(conn)
    print("Deleted from favourites")


a = ("Julia",   "Kut",      "Kutashek", "passw", "kutashek@ya.ru", "Russia")
b = ('Nikita',	'Pavlov',	'niknik', 'passw',	'kolbase@mail.ru',	'Bangladesh')
c = ('Vasya',	'Ganin',	'pikNick',  'passw',	'pikNick@mail.ru',	'Bangladesh')
d = ('Luci',	'Liu',	'Lucinda23',  'passw',	'Lucinda23@fail.ru',	'Canada')
film1 = ('Титаник', 1997, ['мелодрама', 'история', 'триллер', 'драма'], ['США', 'Мексика'])
film2 = ('Титаник', 2012, ['документальный', 'драма'], ['Россия'])
film3 = ('Бэтмен: Начало', 2005, ['боевик', 'фантастика', 'приключения', 'драма'], ['США', 'Великобритания'])

if __name__ == "__main__":
    deploy_db(config_deploy)      # работает
    # create_user(d)                # работает
    # login_user("niknik","passw")    # работает
    # search_user("nekituall")       # работает
    # ask_friend((3, 1))          # работает
    # show_friends(1, "asked")    # работает
    # confirm_friend((3,2))       # работает
    # reject_friend((3, 2))       # работает
    # delete_friend((3, 4))       # работает
    # search_film("Титаник")      # работает
    # add_film(film1)               # работает
    # add_favourite((3, 3, "2023-04-11", 5, "что надо"))       #работает , если дата-строчка
    # show_favourites(1)
    # delete_favourite((12, 1))       # работает
    pass