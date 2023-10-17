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
    'request': re.compile(r"^.{0,150}$", re.DOTALL),
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

    return render_template(
        "home.html",
        chats = messages.get_latest_messages(
            partners.get_partners(session["username"])
        ),
        find_users = find_users,
        posts = posts.get_posts(),
        registration = request.args.get("registration", False)
    )

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "username" not in session:
        return redirect("/")
    if not partners.check_partner(session["username"], request.args.get("username")):
        return redirect("/home")
    
    chat_id = messages.get_chat_id(session["username"], request.args.get("username"))

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html")
        message = str(escape(request.form["message"])).replace("\r\n", "</br>")
        messages.save_message(chat_id ,session["username"], message)

    sent_messages, sender_id = messages.get_messages(chat_id, session["username"])

    return render_template(
        "chat.html",
        other_chatter = request.args.get("username"),
        messages = sent_messages,
        sender = sender_id)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect("/")
    
    session["profile_username"] = request.args.get("username")

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

    return render_template(
        "profile.html",
        profile = profiles.get_profile(session["profile_username"]),
        partner = partners.check_partner(session["username"], session["profile_username"])
    )
    
@app.route('/profile_picture')
def profile_picture():
    data = profiles.get_profile_picture(request.args.get("username"))
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

    return render_template(
        "edit.html",
        profile = profiles.get_profile(session["username"]),
        languages = db.get_languages(),
        levels = ["Unspecified", "Beginner", "Intermediate", "Fluent"],
        temp_bio = request.args.get("bio")
    )

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
    return render_template(
        "notifications.html",
        notifications = partners.get_requests(session["username"])
    )

@app.route("/request_answer")
def request_answer():
    user_id = request.args.get("id")
    if not user_id:
        other_username = request.args.get("username")
        partners.remove_partner(session["username"], other_username)
        return redirect(f"/profile?username={other_username}")
    partners.change_status(session["username"], user_id, request.args.get("answer"))
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
    content = str(escape(request.form.get("content"))).replace("\r\n", "</br>")
    posts.add_post(session["username"], request.form.get("title"), content)
    return redirect("/home")

@app.route("/add_comment", methods=["POST"])
def add_comment():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html")
    post_id = request.args.get("post_id")
    content = str(escape(request.form.get("content"))).replace("\r\n", "</br>")
    posts.add_comment(post_id, session["username"], content)
    return redirect(f"/open_post?id={post_id}")

@app.route("/delete_account")
def delete_account():
    users.delete_user(session["username"])
    return redirect("/")

# Most important to-do's:
    # data validation to chats, posts and comments, profile pic and bio