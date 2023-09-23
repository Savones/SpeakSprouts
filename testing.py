import random
import string
from db import db
from sqlalchemy.sql import text
import users

def generate_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def create_dummy_users(num_users=10):
    sql = text("SELECT * FROM Users")
    result = db.session.execute(sql).fetchall()

    if len(result) < 10:
        for _ in range(num_users):
            username = generate_random_string()
            users.register(username, username)
        
        db.session.commit()