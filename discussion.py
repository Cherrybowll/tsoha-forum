from db import db
import users
from sqlalchemy.sql import text

def get_topics():
    sql = text("SELECT t.id, t.name, t.limited_access, COALESCE(h.count, 0) tcount, h.latest tlatest, COALESCE(m.count, 0) mcount, m.latest mlatest  FROM topics t LEFT JOIN (SELECT topic_id, COUNT(*) count, MAX(created_at) latest FROM threads GROUP BY topic_id) h ON t.id=h.topic_id LEFT JOIN (SELECT topic_id, COUNT(*) count, MAX(created_at) latest FROM messages GROUP BY topic_id) m ON t.id=m.topic_id WHERE t.visibility=TRUE ORDER BY t.name")
    result = db.session.execute(sql)
    return result.fetchall()

def get_threads(topic_id):
    sql = text("SELECT t.id, t.subject, t.content, t.created_at, t.creator_id, u.name creator_name, COALESCE(m.count, 0) mcount, m.latest mlatest FROM threads t LEFT JOIN users u ON t.creator_id=u.id  LEFT JOIN (SELECT thread_id, COUNT(*) count, MAX(created_at) latest FROM messages GROUP BY thread_id) m ON m.thread_id=t.id WHERE t.topic_id=:topic_id ORDER BY t.created_at")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_messages(thread_id):
    sql = text("SELECT m.id, m.content, m.created_at, m.creator_id, u.name creator_name FROM messages m LEFT JOIN users u ON m.creator_id=u.id WHERE thread_id=:thread_id ORDER BY m.created_at")
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()

#Get topic entry by name or id, searches by id if the parameter is not specified
#Both options needed for the quirky URL system
def get_topic_entry(topic_name="", topic_id=0, by_id=True):
    if by_id:
        sql = text("SELECT id, name, limited_access, visibility FROM topics WHERE id=:topic_id")
        result = db.session.execute(sql, {"topic_id":topic_id})
    else:
        sql = text("SELECT id, name, limited_access, visibility FROM topics WHERE name=:topic_name")
        result = db.session.execute(sql, {"topic_name":topic_name})
    return result.fetchone()

def get_thread_entry(thread_id):
    sql = text("SELECT t.id, t.subject, t.content, t.creator_id, t.topic_id, t.created_at, u.name creator_name, u.admin_role creator_admin FROM threads t LEFT JOIN users u ON t.creator_id=u.id WHERE t.id=:thread_id")
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()

def get_message_entry(message_id):
    sql = text("SELECT m.id, m.content, m.creator_id, m.thread_id, m.topic_id, u.name creator_name, u.admin_role creator_admin FROM messages m LEFT JOIN users u ON m.creator_id=u.id WHERE m.id=:message_id")
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()

def add_message(content, creator_id, thread_id, topic_id):
    sql = text("INSERT INTO messages (content, creator_id, thread_id, topic_id, created_at) VALUES (:content, :creator_id, :thread_id, :topic_id, NOW())")
    db.session.execute(sql, {"content":content, "creator_id":creator_id, "thread_id":thread_id, "topic_id":topic_id})
    db.session.commit()
    return

def add_thread(subject, content, creator_id, topic_id):
    sql = text("INSERT INTO threads (subject, content, creator_id, topic_id, created_at) VALUES (:subject, :content, :creator_id, :topic_id, NOW())")
    db.session.execute(sql, {"subject":subject, "content":content, "creator_id":creator_id, "topic_id":topic_id})
    db.session.commit()
    return

def add_topic(name, limited_access):
    sql = text("INSERT INTO topics (name, limited_access) VALUES (:name, :limited_access)")
    db.session.execute(sql, {"name":name, "limited_access":limited_access})
    db.session.commit()
    return

def delete_message(message_id):
    sql = text("DELETE FROM messages WHERE id=:message_id")
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return

def delete_thread(thread_id):
    sql = text("DELETE FROM threads WHERE id=:thread_id")
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()
    return

def hide_topic(topic_id):
    sql = text("UPDATE topics SET visibility=FALSE WHERE id=:topic_id")
    db.session.execute(sql, {"topic_id":topic_id})
    db.session.commit()
    return

def edit_thread(thread_id, new_subject, new_content):
    sql = text("UPDATE threads SET subject=:new_subject, content=:new_content WHERE id=:thread_id")
    db.session.execute(sql, {"new_subject":new_subject, "new_content":new_content, "thread_id":thread_id})
    db.session.commit()
    return

def edit_message(message_id, new_content):
    sql = text("UPDATE messages SET content=:new_content WHERE id=:message_id")
    db.session.execute(sql, {"new_content":new_content, "message_id":message_id})
    db.session.commit()
    return