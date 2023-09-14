from app import app
from flask import render_template, request, redirect, session
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/open_login")
def open_login():
    return render_template("login.html")

@app.route("/open_register")
def open_register():
    return render_template("register.html")

@app.route("/open_new")
def open_new():
    words = users.getUsernames(session["username"])
    return render_template("new.html", items = words)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        session["username"] = username
        return redirect("/open_new")
    return render_template("login.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    if users.register(username, password):
        session["username"] = username
        return redirect("/open_new")
    return render_template("register.html")

@app.route("/chat", methods=["GET"])
def chat():
    selected_username = request.args.get("username")
    return render_template("chat.html", other_chatter = selected_username)
