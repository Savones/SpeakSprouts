from db import db
from sqlalchemy.sql import text

def request_sent(sender_name, receiver_name):

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
        add_request(sender_id, receiver_id)

def add_request(sender_id, receiver_id):

    message = "Testi"
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

    # notifs_query = text("SELECT user_id1, request_message FROM language_partners WHERE user_id2 = :user_id2")
    
    notifs_query = text(
        "SELECT lp.user_id1, u.username, lp.request_message "
        "FROM language_partners lp "
        "JOIN users u ON lp.user_id1 = u.id "
        "WHERE lp.user_id2 = :user_id2"
    )
    
    notifs = db.session.execute(notifs_query, {"user_id2": id}).fetchall()

    print(notifs)

    return notifs
