
#тут будет Фласк
from flask import Flask, request, render_template, session

app = Flask(__name__)


app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass
    else:
        render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)



