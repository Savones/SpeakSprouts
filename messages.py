from db import db
from sqlalchemy.sql import text

def save_message(sender_name, receiver_name, message):
    pass

    # sql = text("SELECT id FROM users WHERE username <> :username")
    # sender_id = db.session.execute(sql, {"username":sender_name})
    # sql = text("SELECT id FROM users WHERE username <> :username")
    # receiver_name_id = db.session.execute(sql, {"username":receiver_name})

    # sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    # db.session.execute(sql, {"username":username, "password":hash_value})
    # db.session.commit()