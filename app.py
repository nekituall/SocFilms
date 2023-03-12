from flask import Flask, request, render_template, session, redirect, url_for, flash
from model import login_user, show_friends, show_favourites, confirm_friend


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
        confirmed_friends = show_friends(session["username"][0], "confirmed")
        favourites = show_favourites(session["username"][0])
        return render_template('profile.html', asked=asked_friends, confirmed=confirmed_friends, favourites=favourites)
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
            session.permanent = (True, 10)
            print(login_try)
            return redirect(url_for('profile'))
        else:
            error = 'Please check you nickname/password'
    else:
        if "username" in session:
            return redirect(url_for('profile'))
        return render_template('login.html', error=error)


@app.route('/signup')
def signup():
    pass

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/add")
def add():
    if request.method == "POST":
        return "Hello world!"
        # confirm_friend(1)
        # return render_template("about.html")


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)



