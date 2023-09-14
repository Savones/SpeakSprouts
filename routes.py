from app import app
from flask import render_template, request, redirect, session
import users
import messages

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

@app.route("/open_chat")
def open_chat():
    chat_id = messages.get_chat_id(session["username"], request.args.get("username"))
    session["chat_id"] = chat_id
    return redirect(f"/chat?username={request.args.get('username')}")

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

@app.route("/chat", methods=["GET", "POST"])
def chat():
    sent_messages = ["moi", "Tämä on testi viesti", "Saatko näitä??"]
    if request.method == "POST":
        message = request.form["message"]
        messages.save_message(session["chat_id"],session["username"], message)
    return render_template("chat.html", other_chatter=request.args.get("username"), messages=sent_messages)



