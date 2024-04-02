from db import db
import users
from sqlalchemy.sql import text

def get_topics():
    sql = text("SELECT id, name, access_group FROM topics WHERE visibility=TRUE")
    result = db.session.execute(sql)
    return result.fetchall()

def get_threads(topic_id):
    sql = text("SELECT t.id, t.subject, t.created_at, u.name AS creator_name FROM threads t LEFT JOIN users u ON t.creator_id=u.id WHERE t.topic_id=:topic_id")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_messages(thread_id):
    sql = text("SELECT m.id, m.content, m.created_at, u.name AS creator_name FROM messages m LEFT JOIN users u ON m.creator_id=u.id WHERE thread_id=:thread_id")
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()

def get_topic_entry(topic_name):
    sql = text("SELECT id, name, access_group, visibility FROM topics WHERE name=:topic_name")
    result = db.session.execute(sql, {"topic_name":topic_name})
    return result.fetchone()

def get_thread_entry(thread_id):
    sql = text("SELECT id, subject, creator_id, created_at FROM threads WHERE id=:thread_id")
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()
