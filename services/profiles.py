from sqlalchemy.sql import text
from flask import session
from db import db
from services.mod import get_id


def get_profile(username):
    sql = text(
        "SELECT profiles.id, bio FROM profiles "
        "JOIN users ON profiles.user_id = users.id "
        "WHERE users.username = :username"
    )
    profile = db.session.execute(sql, {"username": username}).fetchone()

    sql = text(
        """SELECT ll.language_id, ll.proficiency_level, l.language_name
            FROM language_levels ll
            JOIN languages l ON ll.language_id = l.id
            WHERE ll.user_id = :user_id;"""
    )
    languages = db.session.execute(sql, {"user_id": profile[0]}).fetchall()

    profile_dict = {}
    profile_dict["username"] = username
    profile_dict["bio"] = profile[1]
    profile_dict["languages"] = languages

    return profile_dict


def update_profile(username, updated_profile):
    columns = ["image_data", "bio"]

    for key, value in updated_profile.items():
        if key != "languages" and key in columns:
            sql = text(
                f"UPDATE profiles "
                f"SET {key} = :value "
                f"WHERE user_id = (SELECT id FROM users WHERE username = :username)"
            )
            db.session.execute(
                sql, {"key": key, "value": value, "username": username})
    db.session.commit()


def update_language(language_name, username):
    query = text(
        "SELECT id FROM languages WHERE language_name = :language_name")
    sql = text(
        """
        INSERT INTO language_levels (user_id, language_id, proficiency_level)
        VALUES (:user_id, :language_id, 'Unspecified')
        ON CONFLICT (user_id, language_id) DO NOTHING
        """
    )
    db.session.execute(sql, {
        "user_id": get_id(username),
        "language_id": db.session.execute(query, {"language_name": language_name}).scalar()
    }
    )
    db.session.commit()


def delete_language(language_name, username):
    user_id = get_id(username)
    query = text(
        "SELECT id FROM languages WHERE language_name = :language_name")
    language = db.session.execute(
        query, {"language_name": language_name}).scalar()
    sql = text(
        """DELETE FROM language_levels WHERE language_id =:language_id AND user_id =:user_id"""
    )
    db.session.execute(sql, {"user_id": user_id, "language_id": language})
    db.session.commit()


def update_level(language_id, username, level):
    user_id = get_id(username)
    update_query = text(
        "UPDATE language_levels SET proficiency_level = :level "
        "WHERE user_id = :user_id AND language_id = :language_id"
    )
    db.session.execute(
        update_query, {"level": level, "user_id": user_id, "language_id": language_id})
    db.session.commit()


def add_profile_picture(file):
    data = file.read()
    sql = text(
        "UPDATE profiles "
        "SET image_data = :image_data "
        "WHERE user_id = (SELECT id FROM users WHERE username = :username)"
    )
    db.session.execute(
        sql, {"username": session["username"], "image_data": data})
    db.session.commit()


def get_profile_picture(username):
    sql = text(
        "SELECT image_data FROM profiles "
        "JOIN users ON profiles.user_id = users.id "
        "WHERE users.username = :username")
    result = db.session.execute(sql, {"username": username})
    data = result.fetchone()[0]
    return data
