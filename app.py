from flask import Flask, request, render_template, session, redirect, url_for, flash
from model import login_user, show_friends, show_favourites, search_film, create_user, search_user, confirm_friend


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
        print(asked_friends)
        confirmed_friends = show_friends(session["username"][0], "confirmed")
        print(confirmed_friends)
        favourites = show_favourites(session["username"][0])
        # если возвращается None - то в шаблоне ошибка
        return render_template('profile.html', user=session["username"][1],asked=asked_friends, confirmed=confirmed_friends, favourites=favourites)
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
            flash('You were successfully logged in')
            session["username"] = login_try
            print(login_try)
            return redirect(url_for('profile'))
        else:
            error = 'Please check you nickname/password'
            return render_template('login.html', error=error)
    else:
        if "username" in session:
            return redirect(url_for('profile'))
        return render_template('login.html', error=error)


@app.route('/signup', methods= ["GET", "POST"])
def signup():
    if "username" in session:
        return redirect(url_for('profile'))
    if request.method == "POST" and request.form["name"] and request.form["surname"] and request.form["nickname"] and \
            request.form["passw"] and request.form["email"] and request.form["country"]:
        data = request.form.values()
        try:
            data = tuple([i for i in data])
            create_user(data)
            return redirect(url_for("login"))
        except:
            return render_template('signup.html')
    return render_template('signup.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/searchfilm", methods=["GET", "POST"])
def search_kino():
    if "username" in session:
        if request.method == 'POST' and request.form["filmname"]:
            res = search_film(request.form["filmname"])
            return render_template("searchfilm.html", films=res)
        else:
            return render_template("searchfilm.html")
    else:
        if request.method == 'POST' and request.form["filmname"]:
            res = search_film(request.form["filmname"])
            return render_template("searchfilm4all.html", films=res)
        return render_template("searchfilm4all.html",)



@app.route("/searchuser", methods=["GET", "POST"])
def search_friend():
    if "username" in session:
        if request.method == "POST":
            res = search_user(request.form["username"])
            return render_template("searchuser.html", user=res)
        return render_template("searchuser.html")

@app.route("/add_favourite")
def add_favourite():
    if request.method == "GET":
        print(request.query_string.split())
        return "Added!"
        # confirm_friend(1)
        # return render_template("about.html")


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)



