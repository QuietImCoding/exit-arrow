from flask import Flask, render_template, url_for, redirect, session, request
from utils import dbUtils
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    if "user" in session:
        return redirect( url_for('auth') )
    return render_template("index.html", logged_in="user" in session)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/auth', methods=['GET','POST'])
def auth():
    if request.method=="GET":
        return render_template("auth.html")
    else:
        if request.form.get("action") == "login":
            user = request.form["LIuname"]
            pwd = request.form["LIpass"]
            hashObj = hashlib.sha1()
            hashObj.update(pwd)
            pwd = hashObj.hexdigest()
            if dbUtils.loginAuth(user, pwd) == 0:
                session["user"] = user
                return redirect(url_for("index"))
                return render_template("auth.html", extra = "LOGIN INCORRECT")
        else: #assert action == register
            user = request.form["SUuname"]
            pwd = request.form["SUpass"]
            confirm = request.form["SUconfirm"]
            if dbUtils.registerAuth(user, pwd, confirm) == 0:
                hashObj = hashlib.sha1()
                hashObj.update(pwd)
                pwd = hashObj.hexdigest()
                dbUtils.addUser(user, pwd, pic)
                session["user"] = user #store session                                               
                return redirect(url_for("index"))
            return render_template("auth.html")


@app.route('/<username>')
def user(username):
    return render_template("user.html")


@app.route('/kill', methods=["POST"])
def kill():
    if method == "POST":
        victimQR = request.form.get("victimQR")
        if validKill(session["user"], victimQR):
            return "ye killed him bub !!!!!"
        else:
            return "nope xddd"

if __name__ == "__main__":
    app.secret_key="DOGGO"
    app.run(debug=True)
