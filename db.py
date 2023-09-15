from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import json
from sqlalchemy.sql import text

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

def read_json():
    # should only be added if doesn't exist yet
    with open('datasets/languages.json', 'r') as file:
        data = json.load(file)

    for item in data:
        language_name = item['name']
        native_name = item['native']
        iso_639_1_code = item['code']
        sql = text(
            "INSERT INTO languages (language_name, native_name, iso_639_1_code) VALUES (:language_name, :native_name, :iso_639_1_code)"
        )
        db.session.execute(sql, {"language_name":language_name, "native_name":native_name, "iso_639_1_code":iso_639_1_code})
    db.session.commit()
        
