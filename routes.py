from app import app
from flask import redirect, render_template, request, url_for
import users
import discussion

@app.route("/")
def index():
    topics = discussion.get_topics()
    return render_template("index.html", topics=topics)

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
    topic = discussion.get_topic_entry(topic_name)
    threads = discussion.get_threads(topic.id)
    #TODO: check user topic access rights
    if request.method == "GET":
        return render_template("topic.html", threads=threads, topic=topic)
    if request.method == "POST":
        new_thread_name = request.form["new_thread_name"]
        discussion.add_thread(new_thread_name, users.user_id(), topic.id)
        return redirect(url_for("open_topic", topic_name=topic.name))

@app.route("/forum/<string:topic_name>/<int:thread_id>", methods=["GET", "POST"])
def open_thread(thread_id, topic_name):
    topic = discussion.get_topic_entry(topic_name)
    thread = discussion.get_thread_entry(thread_id)
    messages = discussion.get_messages(thread_id)
    #TODO: ensure that id for topic matches thread's topic_id
    #TODO: check user topic AND thread access rights
    if request.method == "GET":
        return render_template("thread.html", messages=messages, thread=thread, topic=topic)
    if request.method == "POST":
        new_content = request.form["new_message"]
        discussion.add_message(new_content, users.user_id(), thread.id, topic.id)
        return redirect(url_for("open_thread", thread_id=thread.id, topic_name=topic.name))

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