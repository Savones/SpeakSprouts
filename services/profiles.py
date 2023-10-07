from sqlalchemy.sql import text
from db import db
from services.mod import get_id
from flask import session

def get_profile(username):
    sql = text("SELECT * FROM profiles WHERE username = :username")
    profile = db.session.execute(sql, {"username":username}).fetchone()

    sql = text(
        """SELECT ll.language_id, ll.proficiency_level, l.language_name
            FROM language_levels ll
            JOIN languages l ON ll.language_id = l.id
            WHERE ll.user_id = :user_id;"""
    )
    languages = db.session.execute(sql, {"user_id":profile[0]}).fetchall()

    profile_dict = {}
    profile_dict["username"] = profile[1]
    profile_dict["bio"] = profile[3]
    profile_dict["color"] = profile[4]
    profile_dict["languages"] = languages

    return profile_dict

def update_profile(username, updated_profile):
    for key, value in updated_profile.items():
        if key == "languages":
            pass

        else:
            sql = text(f"UPDATE profiles SET {key} = :value WHERE username = :username")
            db.session.execute(sql, {"key":key, "value":value, "username":username})
    db.session.commit()

def update_language(language_name, username):
    user_id = get_id(username)
    query = text("SELECT id FROM languages WHERE language_name = :language_name")
    language = db.session.execute(query, {"language_name": language_name}).scalar()
    sql = text(
        """INSERT INTO language_levels (user_id, language_id, proficiency_level)
        VALUES (:user_id, :language_id, 'Unspecified')
        ON CONFLICT (user_id, language_id) DO NOTHING"""
    )
    db.session.execute(sql, {"user_id":user_id, "language_id":language})
    db.session.commit()

def delete_language(language_name, username):
    user_id = get_id(username)
    query = text("SELECT id FROM languages WHERE language_name = :language_name")
    language = db.session.execute(query, {"language_name": language_name}).scalar()
    sql = text(
        """DELETE FROM language_levels WHERE language_id =:language_id AND user_id =:user_id"""
    )
    db.session.execute(sql, {"user_id":user_id, "language_id":language})
    db.session.commit()

def update_level(language_id, username, level):
    user_id = get_id(username)
    update_query = text(
            "UPDATE language_levels SET proficiency_level = :level "
            "WHERE user_id = :user_id AND language_id = :language_id"
        )
    db.session.execute(update_query, {"level": level, "user_id": user_id, "language_id": language_id})
    db.session.commit()

def add_profile_picture(file):
    data = file.read()
    sql = text("UPDATE profiles SET image_data = :image_data WHERE username = :username")
    db.session.execute(sql, {"username":session["username"], "image_data":data})
    db.session.commit()

def get_profile_picture(username):
    sql = text("SELECT image_data FROM profiles WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    data = result.fetchone()[0]
    return data