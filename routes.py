from app import app
from flask import render_template, request, redirect, session, make_response
import users
import messages
import profiles
import db
import json
import partners

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
    words2 = users.getUsernames(session["username"])
    return render_template("new.html", items = words, also_items = words2)

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
    if request.method == "POST":
        message = request.form["message"]
        messages.save_message(session["chat_id"],session["username"], message)
    sent_messages, sender_id = messages.get_messages(session["chat_id"],session["username"])
    return render_template("chat.html", other_chatter=request.args.get("username"), messages=sent_messages, sender = sender_id)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        session["profile_username"] = request.args.get("username")
        profile_info = profiles.get_profile(session["profile_username"])
        return render_template("profile.html", profile=profile_info)
    elif request.method == "POST":
        updated_profile = {}
        for key, value in request.form.items():
            if key == "languages_known":
                updated_profile[key] = json.dumps(request.form.getlist("languages_known"))
            else:
                updated_profile[key] = value
        print(updated_profile)
        profiles.update_profile(session["username"], updated_profile)
        return redirect("/profile?username=" + session["username"])

@app.route("/edit_profile")
def edit_profile():
    profile_info = profiles.get_profile(session["username"])
    languages = db.get_languages()
    return render_template("edit.html", profile = profile_info, languages = languages)

@app.route("/sent_request", methods=["GET", "POST"])
def sent_request():
    message = request.form.get("message")
    partners.request_sent(session["username"], session["profile_username"], message)
    return redirect("/open_new")

@app.route("/notifs")
def notifs():
    notifs = partners.get_requests(session["username"])
    return render_template("notifs.html", notifs = notifs)

@app.route("/request_answer")
def request_answer():
    answer = request.args.get("answer")
    user_id = request.args.get("id")
    partners.change_status(session["username"], user_id, answer)
    return redirect("/notifs")

# For security

# response = make_response(render_template("login.html"))
# response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
# return response

# add checks for the right to open a page