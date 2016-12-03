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

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/<username>')
def user(username):
    return render_template("user.html")

@app.route('/kill')
def kill():
    return render_template("getKill.html")


if __name__ == "__main__":
    app.run(debug=True)
