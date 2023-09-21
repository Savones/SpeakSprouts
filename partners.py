from db import db
from sqlalchemy.sql import text

def request_sent(sender_id, receiver_id):

    partner_id_query = text(
        "SELECT id FROM language_partners WHERE user_id1 = :user_id1 AND user_id2 = :user_id2 FOR UPDATE"
    )

    partner_id = db.session.execute(
        partner_id_query, {"user_id1": sender_id, "user_id2": receiver_id}
    ).scalar()

    message = "Testi"
    status = "Pending"

    if partner_id is None:
        print("is none")
        insert_partner = text(
            "INSERT INTO language_partners (user_id1, user_id2, request_status, request_message) VALUES (:user_id1, :user_id2, :status, :message)"
        )

        db.session.execute(
            insert_partner, {"user_id1": sender_id, "user_id2": receiver_id, "status": status, "message": message}
        )

        db.session.commit()

    else:
        print("is not none")