from sqlalchemy.sql import text
from db import db
from services import users

def create_dummy_users():
    sql = text("SELECT * FROM Users")
    result = db.session.execute(sql).fetchall()
    if len(result) < 5:
        usernames = ["Maria", "Mikko", "Petteri", "Jaana", "Alisa", "Katariina", "Jaakko", "Miia", "Matti-Pekka", "Anniina"]
        for username in usernames:
            users.register(username, username)
        db.session.commit()
