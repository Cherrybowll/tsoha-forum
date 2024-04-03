from db import db
import users
from sqlalchemy.sql import text

def get_topics():
    sql = text("SELECT id, name, access_group FROM topics WHERE visibility=TRUE ORDER BY name")
    result = db.session.execute(sql)
    return result.fetchall()

def get_threads(topic_id):
    sql = text("SELECT t.id, t.subject, t.created_at, u.name AS creator_name FROM threads t LEFT JOIN users u ON t.creator_id=u.id WHERE t.topic_id=:topic_id ORDER BY t.created_at")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_messages(thread_id):
    sql = text("SELECT m.id, m.content, m.created_at, u.name AS creator_name FROM messages m LEFT JOIN users u ON m.creator_id=u.id WHERE thread_id=:thread_id ORDER BY m.created_at")
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

def add_message(content, creator_id, thread_id, topic_id):
    sql = text("INSERT INTO messages (content, creator_id, thread_id, topic_id, created_at) VALUES (:content, :creator_id, :thread_id, :topic_id, NOW())")
    db.session.execute(sql, {"content":content, "creator_id":creator_id, "thread_id":thread_id, "topic_id":topic_id})
    db.session.commit()
    return

def add_thread(subject, creator_id, topic_id):
    sql = text("INSERT INTO threads (subject, creator_id, topic_id, created_at) VALUES (:subject, :creator_id, :topic_id, NOW())")
    db.session.execute(sql, {"subject":subject, "creator_id":creator_id, "topic_id":topic_id})
    db.session.commit()
    return

def add_topic(name, access_group, visibility):
    sql = text("INSERT INTO topics (name, access_group, visibility) VALUES (:name, :access_group, :vsibility)")
    db.session.execute(sql, {"name":name, "access_group":access_group, "visibility":visibility})
    db.session.commit()
    return               