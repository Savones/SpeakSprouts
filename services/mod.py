from sqlalchemy.sql import text
from db import db


def get_id(username):
    id_query = text("SELECT id FROM users WHERE username = :username")
    user_id = db.session.execute(id_query, {"username": username}).scalar()
    return user_id
