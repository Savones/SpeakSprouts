from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db
from flask import session

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        pass
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return True
    return False

def register(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        createUser(username, password)
        return True
    return False

def createUser(username, password):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

def getUsernames(username):
    sql = text("SELECT username FROM users WHERE username <> :username")
    result = db.session.execute(sql, {"username":username})
    return result

def addChat(username, otherUsername):
    pass