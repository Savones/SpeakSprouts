from db import db
from sqlalchemy.sql import text

def get_id(username):
    id_query = text("SELECT id FROM users WHERE username = :username")
    id = db.session.execute(id_query, {"username": username}).scalar()
    return id