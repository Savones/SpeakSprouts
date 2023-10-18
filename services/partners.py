from sqlalchemy.sql import text
from db import db
from services import messages
from services.mod import get_id 

def request_sent(sender_name, receiver_name, message):

    sender_id = get_id(sender_name)
    receiver_id = get_id(receiver_name)

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
            """
            UPDATE language_partners 
            SET request_status = 'Pending', request_message = :message 
            WHERE id = :partner_id
            """
        )
        db.session.execute(
            update_status_query, {"partner_id": partner_id, "message": message}
        )
        db.session.commit()

def add_request(sender_id, receiver_id, message):
    status = "Pending"
    insert_partner = text(
            """
            INSERT INTO language_partners (user_id1, user_id2, request_status, request_message) 
            VALUES (:user_id1, :user_id2, :status, :message)
            """
        )
    db.session.execute(
            insert_partner, {"user_id1": sender_id, "user_id2": receiver_id, "status": status, "message": message}
        )
    db.session.commit()

def get_requests(username):
    user_id = get_id(username)

    notifs_query = text(
        "SELECT lp.user_id1, u.username, lp.request_message "
        "FROM language_partners lp "
        "JOIN users u ON lp.user_id1 = u.id "
        "WHERE lp.request_status = :status AND lp.user_id2 = :user_id2"
    )
    notifs = db.session.execute(notifs_query, {"user_id2": user_id, "status": "Pending"}).fetchall()
    return notifs

def change_status(username, user_id2, answer):
    user_id1 = get_id(username)

    exists_query = text(
        "SELECT EXISTS (SELECT 1 FROM language_partners WHERE (user_id1 = :user_id1 AND user_id2 = :user_id2))"
    )
    row_exists = db.session.execute(exists_query, {"user_id1": user_id1, "user_id2": user_id2}).scalar()

    if not row_exists:
        status = "Accepted" if answer == "accepted" else "Rejected"
        insert_query = text(
            """
            INSERT INTO language_partners (user_id1, user_id2, request_status, request_message) 
            VALUES (:user_id1, :user_id2, :status, '')
            """
        )
        db.session.execute(insert_query, {"user_id1": user_id1, "user_id2": user_id2, "status": status})
    else:
        status = "Accepted" if answer == "accepted" else "Rejected"
        update_query = text(
            """
            UPDATE language_partners 
            SET request_status = :status 
            WHERE (user_id1 = :user_id1 AND user_id2 = :user_id2) 
            OR (user_id1 = :user_id2 AND user_id2 = :user_id1)
            """
        )
        db.session.execute(update_query, {"user_id1": user_id1, "user_id2": user_id2, "status": status})

    update_query = text(
            """
            UPDATE language_partners 
            SET request_status = :status 
            WHERE (user_id1 = :user_id1 AND user_id2 = :user_id2) 
            OR (user_id1 = :user_id2 AND user_id2 = :user_id1)
            """
        )
    db.session.execute(update_query, {"user_id1": user_id2, "user_id2": user_id1, "status": status})
    db.session.commit()

    name_query = text("SELECT username FROM users WHERE id = :id")
    username2 = db.session.execute(name_query, {"id": user_id2}).scalar()

    if answer == 'accepted':
        messages.get_chat_id(username, username2)

def get_partners(username):
    user_id = get_id(username)
    if user_id is None:
        return []
    partners_query = text(
        """
        SELECT u.username, c.id
        FROM language_partners lp 
        JOIN users u ON lp.user_id1 = u.id 
        JOIN chats c ON (lp.user_id1 = c.user1_id AND lp.user_id2 = c.user2_id) 
        OR (lp.user_id1 = c.user2_id AND lp.user_id2 = c.user1_id) 
        LEFT JOIN messages m ON m.chat_id = c.id
        WHERE lp.user_id2 = :user_id AND lp.request_status = 'Accepted'
        GROUP BY u.username, c.id 
        ORDER BY MAX(m.timestamp) DESC NULLS LAST;
        """
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
    user_id = get_id(username)

    non_partners_query = text(
        """
        SELECT username FROM users WHERE id NOT IN 
        (SELECT user_id1 FROM language_partners 
        WHERE user_id2 = :user_id AND request_status = 'Accepted') 
        AND id != :user_id
        """
    )
    non_partners = db.session.execute(non_partners_query, {"user_id": user_id}).fetchall()
    return non_partners

def remove_partner(username, username2):
    user2_id = get_id(username2)
    change_status(username, user2_id, "rejected")

def notification_count(username):
    user_id = get_id(username)

    notifs_query = text(
        "SELECT COUNT(*) "
        "FROM language_partners lp "
        "WHERE lp.request_status = :status AND lp.user_id2 = :user_id2"
    )
    notifs_count = db.session.execute(notifs_query, {"user_id2": user_id, "status": "Pending"}).scalar()
    return notifs_count
