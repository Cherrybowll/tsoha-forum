from app import app
from flask import redirect, render_template, request, url_for
import users
import discussion

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        topics = discussion.get_topics()
        return render_template("index.html", topics=topics)
    if request.method == "POST":
        new_topic_name = request.form["new_topic_name"]
        limited_access = request.form.get("limited_access", False)
        if users.check_admin_role():
            discussion.add_topic(new_topic_name, limited_access)
        return redirect(url_for("index"))

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error_message="Käyttäjätunnusta tai salasanaa ei löydy", username=username)

@app.route("/forum/<string:topic_name>", methods=["GET", "POST"])
def open_topic(topic_name):
    topic = discussion.get_topic_entry(topic_name=topic_name, by_id=False)
    threads = discussion.get_threads(topic.id)
    #check user topic access rights
    if topic.limited_access:
        if not users.check_admin_role():
            if not users.check_access_rights(topic.id):
                return "ei lupaa" #ERROR
    if request.method == "GET":
        return render_template("topic.html", threads=threads, topic=topic)
    if request.method == "POST":
        new_thread_name = request.form["new_thread_name"]
        new_thread_content = request.form["new_thread_content"]
        discussion.add_thread(new_thread_name, new_thread_content, users.user_id(), topic.id)
        return redirect(url_for("open_topic", topic_name=topic.name))

@app.route("/forum/<string:topic_name>/<int:thread_id>", methods=["GET", "POST"])
def open_thread(thread_id, topic_name):
    topic = discussion.get_topic_entry(topic_name=topic_name, by_id=False)
    thread = discussion.get_thread_entry(thread_id)
    messages = discussion.get_messages(thread_id)
    #ensure that id for topic matches thread's topic_id
    if topic.id != thread.topic_id:
        return "bad url" #ERROR
    #check user topic access rights
    if topic.limited_access:
        if not users.check_admin_role():
            if not users.check_access_rights(topic.id):
                return "ei lupaa" #ERROR
    if request.method == "GET":
        return render_template("thread.html", messages=messages, thread=thread, topic=topic)
    if request.method == "POST":
        new_message_content = request.form["new_message"]
        discussion.add_message(new_message_content, users.user_id(), thread.id, topic.id)
        return redirect(url_for("open_thread", thread_id=thread.id, topic_name=topic.name))

@app.route("/delete/topic/<int:topic_id>")
def delete_topic(topic_id):
    if not users.check_admin_role():
        return "ei lupaa" #ERROR
    topic = discussion.get_topic_entry(topic_id=topic_id, by_id=True)
    if topic:
        discussion.hide_topic(topic_id)
        return redirect(url_for("index"))
    return "resurssia ei löydy" #ERROR

@app.route("/delete/thread/<int:thread_id>")
def delete_thread(thread_id):
    thread = discussion.get_thread_entry(thread_id)
    if thread:
        topic_name = discussion.get_topic_entry(topic_id=thread.topic_id, by_id=True).name
        if users.check_admin_role() or users.user_id() == thread.creator_id:
            discussion.delete_thread(thread.id)
            return redirect(url_for("open_topic", topic_name=topic_name))
        return "ei lupaa" #ERROR
    return "resurssia ei löydy" #ERROR

@app.route("/delete/message/<int:message_id>")
def delete_message(message_id):
    message = discussion.get_message_entry(message_id)
    if message:
        topic_name = discussion.get_topic_entry(topic_id=message.topic_id, by_id=True).name
        if users.check_admin_role() or users.user_id() == message.creator_id:
            discussion.delete_message(message.id)
            return redirect(url_for("open_thread", thread_id=message.thread_id, topic_name=topic_name))
        return "ei lupaa" #ERROR
    return "resurssia ei löydy" #ERROR

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        #TODO: possible further username/password requirements
        if password1 != password2:
            return render_template("register.html", error_message="Salasanat eivät täsmää", username=username)
        if password1 == "":
            return render_template("register.html", error_message="Salasana ei voi olla tyhjä", username=username)
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", error_message="Rekisteröinti epäonnistui. Käyttäjätunnus saattaa olla jo käytössä.")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")