from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash

def user_id():
    return session.get("user_id", 0)

def check_admin_role():
    return session.get("admin_role", 0)

def get_user_entry(user_id):
    sql = text("SELECT id, name, password, admin_role, created_at, banned, public, bio FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

def add_friend(user1_id, user2_id):
    #Check if user has already been added to friends to avoid duplicate entries
    #Not necessarily needed
    if check_friends(user1_id, user2_id):
        return False
    #Add to friends:
    try:
        sql = text("INSERT INTO friends (user1, user2) VALUES (:user1_id, :user2_id)")
        db.session.execute(sql, {"user1_id":user1_id, "user2_id":user2_id})
        db.session.commit()
    except:
        print("adding friend exception")
        return False
    return True

def remove_friend(user1_id, user2_id):
    try:
        sql = text("DELETE FROM friends WHERE user1=:user1_id AND user2=:user2_id")
        arvo = db.session.execute(sql, {"user1_id":user1_id, "user2_id":user2_id})
        db.session.commit()
    except:
        print("removing friend exception")
        return False
    return

def check_friends(user1_id, user2_id):
    sql = text("SELECT user1, user2 FROM friends WHERE user1=:user1_id AND user2=:user2_id")
    result = db.session.execute(sql, {"user1_id":user1_id, "user2_id":user2_id})
    if result.fetchone():
        return True
    return False

def add_block(user1_id, user2_id):
    if check_blocked(user1_id, user2_id):
        return False
    sql = text("INSERT INTO blocks (user1, user2) VALUES (:user1_id, :user2_id)")
    db.session.execute(sql, {"user1_id":user1_id, "user2_id":user2_id})
    db.session.commit()
    return True

def remove_block(user1_id, user2_id):
    sql = text("DELETE FROM blocks WHERE user1=:user1_id AND user2=:user2_id")
    db.session.execute(sql, {"user1_id":user1_id, "user2_id":user2_id})
    db.session.commit()
    return

def check_blocked(user1_id, user2_id):
    sql = text("SELECT user1, user2 FROM blocks WHERE user1=:user1_id AND user2=:user2_id")
    result = db.session.execute(sql, {"user1_id":user1_id, "user2_id":user2_id})
    if result.fetchone():
        return True
    return False

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
        sql = text("INSERT INTO users (name, password, created_at) VALUES (:name, :password, NOW())")
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
