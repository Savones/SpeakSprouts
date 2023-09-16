from sqlalchemy.sql import text
from db import db

def get_profile(username):
    sql = text("SELECT * FROM profiles WHERE username = :username")
    profile = db.session.execute(sql, {"username":username}).fetchone()

    profile_dict = {}
    profile_dict["username"] = profile[1]
    profile_dict["languages"] = profile[3]
    profile_dict["levels"] = profile[4]
    profile_dict["bio"] = profile[5]
    profile_dict["color"] = profile[6]

    return profile_dict