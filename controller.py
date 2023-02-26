
#тут будет Фласк
from flask import Flask, request, render_template, session

app = Flask(__name__)


app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass
    else:
        render_template("login.html")

app.run(debug=True)



