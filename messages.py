from db import db
from sqlalchemy.sql import text

def get_chat_id(sender_name, receiver_name):
    sender_id_query = text("SELECT id FROM users WHERE username = :username")
    receiver_id_query = text("SELECT id FROM users WHERE username = :username")

    sender_id = db.session.execute(sender_id_query, {"username": sender_name}).scalar()
    receiver_id = db.session.execute(receiver_id_query, {"username": receiver_name}).scalar()

    # Ensures there is only one chat per pair
    if sender_id > receiver_id:
        sender_id, receiver_id = receiver_id, sender_id

    chat_id_query = text(
        "SELECT id FROM chats WHERE user1_id = :user1_id AND user2_id = :user2_id FOR UPDATE"
    )

    chat_id = db.session.execute(
        chat_id_query, {"user1_id": sender_id, "user2_id": receiver_id}
    ).scalar()

    if chat_id is None:
        chat_insert_query = text(
            "INSERT INTO chats (user1_id, user2_id) VALUES (:user1_id, :user2_id) RETURNING id"
        )

        result = db.session.execute(
            chat_insert_query, {"user1_id": sender_id, "user2_id": receiver_id}
        )

        chat_id = result.scalar()
        db.session.commit()

    return chat_id


def save_message(sender_name, receiver_name, message):
    pass

    # sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    # db.session.execute(sql, {"username":username, "password":hash_value})
    # db.session.commit()