from flask import Flask, render_template, url_for, redirect, session
from utils import dbUtils
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    if "user" in session:
        return redirect( url_for('login') )
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.form.get("action") == "login":
        user = request.form["user"]
        pwd = request.form["pass"]
        hashObj = hashlib.sha1()
        hashObj.update(pwd)
        pwd = hashObj.hexdigest()

        if dbUtils.loginAuth(user, pwd) == 0:
            session["user"] = user
            return redirect(url_for("index"))
        return render_template("auth.html", extra = "LOGIN INCORRECT")
    else: #assert action == register
        user = request.form["user"]
        pwd = request.form["pass"]
        confirm = request.form["confirm"]
        pic = request.form["pic"]
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
    return "kek"
    #return render_template("user.html")


@app.route('/kill')
def kill():
    return render_template("getKill.html")


if __name__ == "__main__":
    app.run(debug=True)
