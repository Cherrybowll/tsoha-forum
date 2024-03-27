from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE name=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            return True
        else:
            return False

def register(username, password):
    password_hash = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (name, password, created_at) VALUES (:name, :password, NOW());")
        db.session.execute(sql, {"name":username, "password":password_hash})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["username"]
    del session["user_id"]