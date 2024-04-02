from app import app
from flask import redirect, render_template, request
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

@app.route("/forum/<string:topic_name>")
def open_topic(topic_name):
    topic_entry = discussion.get_topic_entry(topic_name)
    threads = discussion.get_threads(topic_entry.id)
    #TODO: check user topic access rights
    return render_template("topic.html", threads=threads, topic=topic_entry)

@app.route("/forum/<string:topic_name>/<int:thread_id>")
def open_thread(thread_id, topic_name):
    topic_entry = discussion.get_topic_entry(topic_name)
    thread = discussion.get_thread_entry(thread_id)
    messages = discussion.get_messages(thread_id)
    #TODO: ensure that id for topic matches thread's topic_id
    #TODO: check user topic AND thread access rights
    return render_template("thread.html", messages=messages, thread=thread, topic=topic_name)

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