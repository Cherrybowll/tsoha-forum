from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash

def user_id():
    return session.get("user_id", 0)

def check_admin_role():
    return session.get("admin_role", 0)

def get_access_rights():
    uid = user_id()
    if not uid:
        return []
    sql = text("SELECT topic_id FROM accesses WHERE user_id=:uid")
    result = db.session.execute(sql, {"uid":uid})
    return [i[0] for i in result.fetchall()]

def check_access_rights(topic_id):
    if topic_id in session.get("access_rights"):
        return True
    return False

def login(username, password):
    sql = text("SELECT id, name, password, admin_role FROM users WHERE name=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = user.name
        session["admin_role"] = user.admin_role
        session["access_rights"] = get_access_rights()
        print(session.get("access_rights"))
        return True
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
    del session["admin_role"]
    del session["access_rights"]
