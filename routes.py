import json
import io
import re
from flask import render_template, request, redirect, session, send_file
from app import app
import db
import testing
from services import users
from services import messages
from services import profiles
from services import posts
from services import partners

re = {
    'username': re.compile(r"^\w{3,12}$"),
    'password': re.compile(r"^.{6,24}$"),
    'request': re.compile(r"^.{0,50}$"),
}

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/")
def index():
    db.read_json()
    testing.create_dummy_users()
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect("/home")
        success = False
    else:
        success = True
    return render_template("login.html", login = success)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        global re
        if not re["username"].match(request.form["username"]) \
        or not re["password"].match(request.form["password"]) \
        or not request.form["password"] == request.form["confirm_password"]:
            return render_template("error.html")

        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            session["username"] = username
            return redirect("/home?registration=True")
        success = False
    else:
        success = True
    return render_template("register.html", registration = success)

@app.route("/home")
def home():
    registration = request.args.get("registration")
    if not registration:
        registration = False
    partners_info = partners.get_partners(session["username"])
    partners_chat_ids = [id[1] for id in partners_info]
    latest_messages = messages.get_latest_messages(partners_chat_ids)
    message_info = [(partner, latest_messages[i]) for i, partner in enumerate(partners_info)]
    non_partners = partners.get_non_partners(session["username"])
    posts_info = posts.get_posts()
    return render_template("home.html", chats = message_info, find_users = non_partners, posts = posts_info, registration = registration)

@app.route("/open_chat")
def open_chat():
    chat_id = messages.get_chat_id(session["username"], request.args.get("username"))
    session["chat_id"] = chat_id
    return redirect(f"/chat?username={request.args.get('username')}")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        message = request.form["message"]
        messages.save_message(session["chat_id"],session["username"], message)
    sent_messages, sender_id = messages.get_messages(session["chat_id"],session["username"])
    other = request.args.get("username")
    return render_template("chat.html", other_chatter=other, messages=sent_messages, sender = sender_id)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    session["profile_username"] = request.args.get("username")
    result = partners.check_partner(session["username"], session["profile_username"])

    if request.method == "POST":
        file = request.files["file"]
        if file:
            profiles.add_profile_picture(file)
        updated_profile = {}
        for key, value in request.form.items():
            if key == "languages":
                updated_profile[key] = json.dumps(request.form.getlist("languages"))
            else:
                updated_profile[key] = value
        profiles.update_profile(session["username"], updated_profile)

    profile_info = profiles.get_profile(session["profile_username"])
    return render_template("profile.html", profile=profile_info, partner=result)
    
@app.route('/profile_picture')
def profile_picture():
    username = request.args.get("username")
    data = profiles.get_profile_picture(username)
    return send_file(io.BytesIO(data), mimetype='image/jpeg')

@app.route("/edit_profile")
def edit_profile():
    deleted = request.args.get("deleted")
    language = request.args.get("language")
    level = request.args.get("level")
    language_id = request.args.get("id")
    if level and id:
        profiles.update_level(language_id, session["username"], level)
    if language:
        profiles.update_language(language, session["username"])
    if deleted:
        profiles.delete_language(deleted, session["username"])
    profile_info = profiles.get_profile(session["username"])
    languages = db.get_languages()
    levels = ["Unspecified", "Beginner", "Intermediate", "Fluent"]
    return render_template("edit.html", profile = profile_info, languages = languages, levels = levels)

@app.route("/sent_request", methods=["GET", "POST"])
def sent_request():
    message = request.form.get("message")
    global re
    if not re["request"].match(message):
        return render_template("error.html")
    partners.request_sent(session["username"], session["profile_username"], message)
    return redirect("/home")

@app.route("/notifications")
def users_notifications():
    notifications = partners.get_requests(session["username"])
    return render_template("notifications.html", notifications = notifications)

@app.route("/request_answer")
def request_answer():
    answer = request.args.get("answer")
    user_id = request.args.get("id")
    if not user_id:
        username2 = request.args.get("username")
        partners.remove_partner(session["username"], username2)
        return redirect(f"/profile?username={username2}")
    partners.change_status(session["username"], user_id, answer)
    return redirect("/notifications")

@app.route("/open_post")
def open_post():
    post_id = request.args.get("id")
    post_info = "None"
    post_comments = []
    if post_id != "None":
        post_info = posts.get_post_info(post_id)
        post_comments = posts.get_comments(post_id)
    return render_template("post.html", post = post_info, comments = post_comments)

@app.route("/add_post", methods=["POST"])
def add_post():
    title = request.form.get("title")
    author = session["username"]
    content = request.form.get("content")
    posts.add_post(author, title, content)
    return redirect("/home")

@app.route("/add_comment", methods=["POST"])
def add_comment():
    post_id = request.args.get("post_id")
    author = session["username"]
    content = request.form.get("content")
    posts.add_comment(post_id, author, content)
    return redirect(f"/open_post?id={post_id}")

@app.route("/delete_account")
def delete_account():
    users.delete_user(session["username"])
    return redirect("/")
