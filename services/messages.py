from sqlalchemy.sql import text
from datetime import datetime
from db import db
from services.mod import get_id

def get_chat_id(sender_name, receiver_name):
    sender_id = get_id(sender_name)
    receiver_id = get_id(receiver_name)

    # Ensures there is only one chat per pair
    if sender_id > receiver_id:
        sender_id, receiver_id = receiver_id, sender_id

    chat_id_query = text(
        "SELECT id FROM chats WHERE user1_id = :user1_id AND user2_id = :user2_id FOR UPDATE"
    )

    chat_id = db.session.execute(
        chat_id_query, {"user1_id": sender_id, "user2_id": receiver_id}
    ).scalar()

    # Adds the chat to chats tables if doesn't exist yet
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

def save_message(chat_id, sender_username, message):
    sender_id = get_id(sender_username)
    timestamp = datetime.now()

    insert_message = text(
            "INSERT INTO messages (chat_id, sender_id, message_text, timestamp) VALUES (:chat_id, :sender_id, :message_text, :timestamp)"
        )
    
    db.session.execute(
            insert_message, {"chat_id":chat_id, "sender_id":sender_id, "message_text":message, "timestamp":timestamp}
        )
    db.session.commit()

def get_messages(chat_id, username):
    sender_id = get_id(username)

    messages_query = text("SELECT message_text, sender_id, timestamp FROM messages WHERE chat_id = :chat_id")
    messages = db.session.execute(messages_query, {"chat_id": chat_id})
    return messages, sender_id

def query_latest_messages(chat_ids, partners_info):
    latest_messages = []
    for i, chat_id in enumerate(chat_ids):
        message = {}
        latest_message_query = text(
            """
            SELECT messages.message_text, users.username 
            FROM messages 
            JOIN users ON messages.sender_id = users.id 
            WHERE messages.chat_id = :chat_id 
            ORDER BY messages.timestamp DESC 
            LIMIT 1;
            """
        )
        latest_message = db.session.execute(latest_message_query, {"chat_id": chat_id}).fetchone()
        if latest_message:
            message["message"] = latest_message[0]
            message["sender_username"] = latest_message[1]
        message["partner_username"] = partners_info[i][0]
        message["partner_id"] = partners_info[i][1]
        latest_messages.append(message)
    return latest_messages

def get_latest_messages(partners_info):
    partners_chat_ids = [id[1] for id in partners_info]
    latest_messages = query_latest_messages(partners_chat_ids, partners_info)
    return latest_messages