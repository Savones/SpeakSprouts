import json
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

def read_json():
    # Adds the languages from json file to languages table in db
    with open('datasets/languages.json', 'r') as file:
        data = json.load(file)

    sql = text(
                "SELECT * FROM languages"
            )
    result = db.session.execute(sql).scalar()
    if not result:
        for item in data:
            language_name = item['name']
            native_name = item['native']
            iso_639_1_code = item['code']
            sql = text(
                """INSERT INTO languages (language_name, native_name, iso_639_1_code) 
                VALUES (:language_name, :native_name, :iso_639_1_code)"""
            )
            db.session.execute(sql, {
                "language_name":language_name, "native_name":native_name, "iso_639_1_code":iso_639_1_code
                })
    db.session.commit()
        
def get_languages():
    sql = text("SELECT language_name FROM languages ORDER BY language_name")
    languages = db.session.execute(sql).fetchall()
    return languages