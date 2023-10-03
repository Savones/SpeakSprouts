from db import db
from sqlalchemy.sql import text
import services.users as users

def create_dummy_users():
    sql = text("SELECT * FROM Users")
    result = db.session.execute(sql).fetchall()

    if len(result) < 10:
        usernames = ["Maria", "Mikko", "Petteri", "Jaana", "Alisa", "Katariina", "Jaakko", "Miia", "Matti-Pekka", "Anniina"]
        for username in usernames:
            users.register(username, username)
        
        db.session.commit()