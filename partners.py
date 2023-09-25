from db import db
import messages
from sqlalchemy.sql import text

def request_sent(sender_name, receiver_name, message):

    sender_id_query = text("SELECT id FROM users WHERE username = :username")
    receiver_id_query = text("SELECT id FROM users WHERE username = :username")

    sender_id = db.session.execute(sender_id_query, {"username": sender_name}).scalar()
    receiver_id = db.session.execute(receiver_id_query, {"username": receiver_name}).scalar()

    partner_id_query = text(
        "SELECT id FROM language_partners WHERE user_id1 = :user_id1 AND user_id2 = :user_id2 FOR UPDATE"
    )

    partner_id = db.session.execute(
        partner_id_query, {"user_id1": sender_id, "user_id2": receiver_id}
    ).scalar()

    if partner_id is None:
        add_request(sender_id, receiver_id, message)
    else:
        update_status_query = text(
            "UPDATE language_partners SET request_status = 'Pending', request_message = :message WHERE id = :partner_id"
        )
        db.session.execute(
            update_status_query, {"partner_id": partner_id, "message": message}
        )
        db.session.commit()

def add_request(sender_id, receiver_id, message):
    status = "Pending"

    insert_partner = text(
            "INSERT INTO language_partners (user_id1, user_id2, request_status, request_message) VALUES (:user_id1, :user_id2, :status, :message)"
        )

    db.session.execute(
            insert_partner, {"user_id1": sender_id, "user_id2": receiver_id, "status": status, "message": message}
        )

    db.session.commit()

def get_requests(username):
    id_query = text("SELECT id FROM users WHERE username = :username")
    id = db.session.execute(id_query, {"username": username}).scalar()

    notifs_query = text(
        "SELECT lp.user_id1, u.username, lp.request_message "
        "FROM language_partners lp "
        "JOIN users u ON lp.user_id1 = u.id "
        "WHERE lp.request_status = :status AND lp.user_id2 = :user_id2"
    )
    
    notifs = db.session.execute(notifs_query, {"user_id2": id, "status": "Pending"}).fetchall()
    return notifs

def change_status(username, user_id2, answer):
    id_query = text("SELECT id FROM users WHERE username = :username")
    user_id1 = db.session.execute(id_query, {"username": username}).scalar()
    exists_query = text(
        "SELECT EXISTS (SELECT 1 FROM language_partners WHERE (user_id1 = :user_id1 AND user_id2 = :user_id2))"
    )
    row_exists = db.session.execute(exists_query, {"user_id1": user_id1, "user_id2": user_id2}).scalar()

    if not row_exists:
        status = "Accepted" if answer == "accepted" else "Rejected"
        insert_query = text(
            "INSERT INTO language_partners (user_id1, user_id2, request_status, request_message) VALUES (:user_id1, :user_id2, :status, '')"
        )
        db.session.execute(insert_query, {"user_id1": user_id1, "user_id2": user_id2, "status": status})
    else:
        status = "Accepted" if answer == "accepted" else "Rejected"
        update_query = text(
            "UPDATE language_partners SET request_status = :status WHERE (user_id1 = :user_id1 AND user_id2 = :user_id2) OR (user_id1 = :user_id2 AND user_id2 = :user_id1)"
        )
        db.session.execute(update_query, {"user_id1": user_id1, "user_id2": user_id2, "status": status})

    update_query = text(
            "UPDATE language_partners SET request_status = :status WHERE (user_id1 = :user_id1 AND user_id2 = :user_id2) OR (user_id1 = :user_id2 AND user_id2 = :user_id1)"
        )
    db.session.execute(update_query, {"user_id1": user_id2, "user_id2": user_id1, "status": status})

    db.session.commit()

    name_query = text("SELECT username FROM users WHERE id = :id")
    username2 = db.session.execute(name_query, {"id": user_id2}).scalar()

    if answer == 'accepted':
        messages.get_chat_id(username, username2)

def get_partners(username):
    user_id_query = text("SELECT id FROM users WHERE username = :username")
    user_id = db.session.execute(user_id_query, {"username": username}).scalar()

    if user_id is None:
        return []

    partners_query = text(
        "SELECT u.username, c.id "
        "FROM language_partners lp "
        "JOIN users u ON lp.user_id1 = u.id "
        "JOIN chats c ON (lp.user_id1 = c.user1_id AND lp.user_id2 = c.user2_id) OR (lp.user_id1 = c.user2_id AND lp.user_id2 = c.user1_id) "
        "WHERE lp.user_id2 = :user_id AND lp.request_status = 'Accepted'"
    )
    language_partners = db.session.execute(partners_query, {"user_id": user_id}).fetchall()

    return language_partners

def check_partner(username, check_username):
    result = get_partners(username)
    for user in result:
        if user[0] == check_username:
            return True
    return False

def get_non_partners(username):
    user_id_query = text("SELECT id FROM users WHERE username = :username")
    user_id = db.session.execute(user_id_query, {"username": username}).scalar()

    if user_id is None:
        return []

    non_partners_query = text(
        "SELECT username FROM users WHERE id NOT IN "
        "(SELECT user_id1 FROM language_partners WHERE user_id2 = :user_id) "
        "AND id != :user_id"
    )
    non_partners = db.session.execute(non_partners_query, {"user_id": user_id}).fetchall()

    return non_partners