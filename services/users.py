from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db
from services.mod import get_id


def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username": username}).fetchone()
    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return True
    return False


def register(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username": username}).fetchone()
    if not user:
        create_user(username, password)
        add_profile(username)
        return True
    return False


def create_user(username, password):
    hash_value = generate_password_hash(password)
    sql = text(
        "INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()


def add_profile(username):
    user_id = get_id(username)
    sql = text("""INSERT INTO profiles (id, user_id)
               VALUES (:user_id, :user_id)""")
    db.session.execute(sql, {"user_id": user_id})
    db.session.commit()


def delete_user(username):
    user_id = get_id(username)
    if user_id is not None:
        try:
            delete_user_query = text("DELETE FROM users WHERE id = :user_id")
            db.session.execute(delete_user_query, {"user_id": user_id})
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    else:
        return False


def all_users(username):
    sql = text("SELECT username FROM users WHERE username !=:username")
    result = db.session.execute(sql, {"username": username})
    return result


def search_users(search: str, username):
    found = True
    sql = text(
        """
        SELECT username
        FROM users
        WHERE UPPER(username) LIKE '%' || :search || '%'
        AND username !=:username
        """
    )
    users = db.session.execute(sql, {
        "search": search.upper(),
        "username": username
    }
    ).fetchall()
    if not users:
        users = all_users(username)
        found = False
    return users, found
