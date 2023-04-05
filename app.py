from flask import Flask, request, render_template, session, redirect, url_for, flash
from model import login_user, show_friends, show_favourites, search_film, create_user, search_user, confirm_friend, \
    ask_friend, reject_friend, add_favourites

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    if "username" in session:
    # сюда надо передавать id пользователя
        asked_friends = show_friends(session["username"][0], "asked")
        # print(asked_friends)
        confirmed_friends = show_friends(session["username"][0], "confirmed")
        #РЕШЕНО! проблема с отображением друзей у обоих пользователей
        # print(confirmed_friends)
        favourites = show_favourites(session["username"][0])
        #РЕШЕНО! если возвращается None - то в шаблоне ошибка
        return render_template('profile.html', user=session["username"][1], asked=asked_friends, confirmed=confirmed_friends, favourites=favourites)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        nick = request.form['username']
        passw = request.form['password']
        login_try = login_user(nick, passw)
        if login_try != None:
            session["username"] = login_try

            return redirect(url_for('profile'))
        else:
            error = 'Пожалуйста проверьте логин/пароль'
            return render_template('login.html', error=error)
    else:
        if "username" in session:
            return redirect(url_for('profile'))
        return render_template('login.html', error=error)


@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if "username" in session:
        return redirect(url_for('profile'))
    if request.method == "POST" and request.form["name"] and request.form["surname"] and request.form["nickname"] and \
            request.form["passw"] and request.form["email"] and request.form["country"]:
        data = request.form.values()
        data = tuple([i for i in data])
        res = create_user(data)
        if res is None:
            error = "Пользователь с таким никнеймом уже существует"
            return render_template('signup.html', error=error)
        else:
            return redirect(url_for("login"))
    return render_template('signup.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/searchfilm", methods=["GET", "POST"])
def search_kino():
    error = "Таких фильмов не нашли.."
    if "username" in session:
        if request.method == 'POST':
            res = search_film(request.form["filmname"])
            if len(res) != 0:
                return render_template("searchfilm.html", films=res)
            else:
                return render_template("searchfilm.html", error=error)
        else:
            return render_template("searchfilm.html")
    else:
        if request.method == 'POST' and request.form["filmname"]:
            res = search_film(request.form["filmname"])
            if len(res) != 0:
                return render_template("searchfilm4all.html", films=res)
            else:
                return render_template("searchfilm4all.html", error=error)
        return render_template("searchfilm4all.html",)



@app.route("/searchuser", methods=["GET", "POST"])
def search_friend():
    if "username" in session:
        if request.method == "POST":
            if len(request.form["username"]) > 1:
                res = search_user(request.form["username"])
                if res is not None:
                    return render_template("searchuser.html", users=res)
                else:
                    entry = request.form["username"]
                    return render_template("searchuser.html", error="Таких пользователей не нашли")
            else:
                return render_template("searchuser.html", error="Проверьте ваш ввод")
        if "error" in session:
            error = session["error"]
            del session["error"]
            return render_template("searchuser.html", error=error)
        return render_template("searchuser.html")


@app.route("/ask_friend", methods=["GET"])
def ask_for_friend():
    if "username" in session:
        main = session["username"][0]
        # print(main)
        fr = request.args.get("username")
        # print(fr)
        if int(main) != int(fr):
            ask_friend((main, fr))
        else:
            session["error"] = "Вы не можете добавить себя"
            return redirect(url_for("search_friend"))
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('index'), code=405)


@app.route("/add_favourite", methods=["GET", "POST"])
def add_favourite():
    if "username" in session:
        if request.method == "GET":
            session["idfilm"] = request.args["idfilm"]
            return render_template("add_favourite.html")
        #     print(request.query_string)
        #     # print(request.args.get("filmname"))
        #     if "filmid" in request.args:
        #         data = request.args["filmgenre"]
        #         # print((data['filmid']))
        #         # print((data['filmyear']))
        #         # print((data['filmgenre']))
        #         # print((data['filmcountry']))
        #         # print(data['filmcountry'].strip("[]' "))
        if request.method == "POST":
            # print(request.form["date"])
            add_favourites((session["username"][0], session["idfilm"], request.form["date"], request.form["rating"],
                          request.form["comment"]))
            flash("Added!")
            return redirect(url_for("profile"))
        else:
            return None
    else:
        return redirect(url_for('login'))


@app.route("/confirm_friend")
def confirm():
    if "username" in session:
        if request.method == "GET" and request.args.get("conf_user"):
            # print(session["username"][0])
            # print(request.args.get("conf_user"))
            confirm_friend((session["username"][0], int(request.args.get("conf_user"))))
            return redirect(url_for("profile"))

@app.route("/reject_friend")
def reject():
    if "username" in session:
        if request.method == "GET" and request.args.get("rej_user"):
            # print(session["username"][0])
            # print(request.args.get("rej_user"))
            reject_friend((session["username"][0], int(request.args.get("rej_user"))))
            return redirect(url_for("profile"))


@app.route("/view_friend")
def view_friend():
    if "username" in session:
        if request.method == "GET" and request.args.get("iduser"):
            favourites = show_favourites(request.args.get("iduser"))
            return render_template("view_friend.html", favourites=favourites, user=session["username"][1])


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)



