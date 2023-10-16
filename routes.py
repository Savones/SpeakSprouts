import json
import secrets
import io
import re
from flask import render_template, request, redirect, session, send_file, escape
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
    'request': re.compile(r"^(.|[\n]){0,150}$"),
}

@app.after_request
def after_request(response):
    session["notifications"] = partners.notification_count(session["username"]) if "username" in session else 0
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
            session["csrf_token"] = secrets.token_hex(16)
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
    if "username" not in session:
        return redirect("/")
    try:
        find_users = users.search_users(request.args["query"])
    except:
        find_users = users.all_users(session["username"])

    registration = request.args.get("registration", False)

    partners_info = partners.get_partners(session["username"])
    message_info = messages.get_latest_messages(partners_info)
    posts_info = posts.get_posts()
    return render_template("home.html", chats = message_info, find_users = find_users, posts = posts_info, registration = registration)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "username" not in session:
        return redirect("/")
    
    chat_id = messages.get_chat_id(session["username"], request.args.get("username"))    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html")
        message = request.form["message"]
        message = str(escape(message)).replace("\r\n", "</br>")
        messages.save_message(chat_id ,session["username"], message)
    sent_messages, sender_id = messages.get_messages(chat_id, session["username"])
    other = request.args.get("username")
    if not partners.check_partner(session["username"], other):
        return redirect("/home")
    return render_template("chat.html", other_chatter=other, messages=sent_messages, sender = sender_id)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect("/")
    
    session["profile_username"] = request.args.get("username")
    result = partners.check_partner(session["username"], session["profile_username"])

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html")
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
    if "username" not in session:
        return redirect("/")
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
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html")
    message = request.form.get("message")
    global re
    if not re["request"].match(message):
        return render_template("error.html")
    partners.request_sent(session["username"], session["profile_username"], message)
    return redirect("/home")

@app.route("/notifications")
def users_notifications():
    if "username" not in session:
        return redirect("/")
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
    if "username" not in session:
        return redirect("/")
    post_id = request.args.get("id")
    post_info = "None"
    post_comments = []
    if post_id != "None":
        post_info = posts.get_post_info(post_id)
        post_comments = posts.get_comments(post_id)
    return render_template("post.html", post = post_info, comments = post_comments)

@app.route("/add_post", methods=["POST"])
def add_post():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html")
    title = request.form.get("title")
    author = session["username"]

    content = request.form.get("content")
    content = str(escape(content)).replace("\r\n", "</br>")

    posts.add_post(author, title, content)
    return redirect("/home")

@app.route("/add_comment", methods=["POST"])
def add_comment():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html")
    post_id = request.args.get("post_id")
    author = session["username"]

    content = request.form.get("content")
    content = str(escape(content)).replace("\r\n", "</br>")

    posts.add_comment(post_id, author, content)
    return redirect(f"/open_post?id={post_id}")

@app.route("/delete_account")
def delete_account():
    users.delete_user(session["username"])
    return redirect("/")

# Most important to-do's:
    # changing urls, especially to chat?username="name"
    # test csrf protection
    # line breaks should be allowed
    # data validation to chats, posts and comments, profile pic and bio