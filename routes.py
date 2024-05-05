from app import app
from flask import redirect, render_template, request, url_for, abort
import users
import discussion
import utilities
from datetime import datetime

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        topics = discussion.get_topics()
        return render_template("index.html", topics=topics)
    if request.method == "POST":
        new_topic_name = request.form["new_topic_name"]
        limited_access = request.form.get("limited_access", False)
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        if users.check_admin_role():
            if len(new_topic_name) == 0:
                return render_template("error.html", error_message="Aiheen nimi ei voi olla tyhjä")
            discussion.add_topic(new_topic_name, limited_access)
        return redirect(url_for("index"))

@app.route("/forum/<string:topic_name>", methods=["GET", "POST"])
def open_topic(topic_name):
    topic = discussion.get_topic_entry(topic_name=topic_name, by_id=False)
    threads = discussion.get_threads(topic.id)
    #check user topic access rights
    if topic.limited_access:
        if not users.check_admin_role():
            if not users.check_access_rights(topic.id):
                return render_template("error.html", error_message="Ei lupaa käyttää resurssia")
    blocks = users.get_blocks(users.user_id())
    if request.method == "GET":
        return render_template("topic.html", threads=threads, topic=topic, blocks=blocks)
    if request.method == "POST":
        new_thread_subject = request.form["new_thread_subject"]
        new_thread_content = request.form["new_thread_content"]
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        if len(new_thread_subject) == 0:
                return render_template("error.html", error_message="Ketjun nimi ei voi olla tyhjä")
        discussion.add_thread(new_thread_subject, new_thread_content, users.user_id(), topic.id)
        return redirect(url_for("open_topic", topic_name=topic.name))

@app.route("/forum/<string:topic_name>/<int:thread_id>", methods=["GET", "POST"])
def open_thread(thread_id, topic_name):
    topic = discussion.get_topic_entry(topic_name=topic_name, by_id=False)
    thread = discussion.get_thread_entry(thread_id)
    messages = discussion.get_messages(thread_id)
    #ensure that id for topic matches thread's topic_id
    if topic.id != thread.topic_id:
        return render_template("error.html", error_message="Resurssia ei löydy")
    #check user topic access rights
    if topic.limited_access:
        if not users.check_admin_role():
            if not users.check_access_rights(topic.id):
                return render_template("error.html", error_message="Ei lupaa käyttää resurssia")
    blocks = users.get_blocks(users.user_id())
    if request.method == "GET":
        return render_template("thread.html", messages=messages, thread=thread, topic=topic, blocks=blocks)
    if request.method == "POST":
        new_message_content = request.form["new_message"]
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        if len(new_message_content) == 0:
                return render_template("error.html", error_message="Viesti ei voi olla tyhjä")
        discussion.add_message(new_message_content, users.user_id(), thread.id, topic.id)
        return redirect(url_for("open_thread", thread_id=thread.id, topic_name=topic.name))

@app.route("/delete/topic/<int:topic_id>")
def delete_topic(topic_id):
    if not users.check_admin_role():
        return render_template("error.html", error_message="Ei lupaa käyttää resurssia")
    topic = discussion.get_topic_entry(topic_id=topic_id, by_id=True)
    if topic:
        discussion.hide_topic(topic_id)
        return redirect(url_for("index"))
    return render_template("error.html", error_message="Resurssia ei löydy")

@app.route("/delete/thread/<int:thread_id>")
def delete_thread(thread_id):
    thread = discussion.get_thread_entry(thread_id)
    if thread:
        topic_name = discussion.get_topic_entry(topic_id=thread.topic_id, by_id=True).name
        if users.check_admin_role() or users.user_id() == thread.creator_id:
            discussion.delete_thread(thread.id)
            return redirect(url_for("open_topic", topic_name=topic_name))
        return render_template("error.html", error_message="Ei lupaa käyttää resurssia")
    return render_template("error.html", error_message="Resurssia ei löydy")

@app.route("/delete/message/<int:message_id>")
def delete_message(message_id):
    message = discussion.get_message_entry(message_id)
    if message:
        topic_name = discussion.get_topic_entry(topic_id=message.topic_id, by_id=True).name
        if users.check_admin_role() or users.user_id() == message.creator_id:
            discussion.delete_message(message.id)
            return redirect(url_for("open_thread", thread_id=message.thread_id, topic_name=topic_name))
        return render_template("error.html", error_message="Ei lupaa käyttää resurssia")
    return render_template("error.html", error_message="Resurssia ei löydy")

@app.route("/edit/thread/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):
    thread = discussion.get_thread_entry(thread_id)
    if not thread:
        return render_template("error.html", error_message="Resurssia ei löydy")
    if not (users.check_admin_role() or users.user_id() == thread.creator_id):
        return render_template("error.html", error_message="Ei lupaa käyttää resurssia")
    #Get topic_name for the funny url system
    topic_name = discussion.get_topic_entry(topic_id=thread.topic_id, by_id=True).name
    
    if request.method == "GET":
        return render_template("edit_thread.html", thread=thread)
    
    if request.method == "POST":
        edited_thread_subject = request.form["edited_thread_subject"]
        edited_thread_content = request.form["edited_thread_content"]
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        if len(edited_thread_subject) == 0:
                return render_template("error.html", error_message="Ketjun nimi ei voi olla tyhjä")
        discussion.edit_thread(thread.id, edited_thread_subject, edited_thread_content)
        return redirect(url_for("open_thread", thread_id=thread.id, topic_name=topic_name))

@app.route("/edit/message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    message = discussion.get_message_entry(message_id)
    if not message:
        return render_template("error.html", error_message="Resurssia ei löydy")
    if not (users.check_admin_role() or users.user_id() == message.creator_id):
        return render_template("error.html", error_message="Ei lupaa käyttää resurssia")
    #Get topic_name for the funny url system again
    topic_name = discussion.get_topic_entry(topic_id=message.topic_id, by_id=True).name

    if request.method == "GET":
        return render_template("edit_message.html", message=message)
    
    if request.method == "POST":
        edited_message_content = request.form["edited_message_content"]
        if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
        if len(edited_message_content) == 0:
                return render_template("error.html", error_message="Viesti ei voi olla tyhjä")
        discussion.edit_message(message.id, edited_message_content)
        return redirect(url_for("open_thread", thread_id=message.thread_id, topic_name=topic_name))

@app.route("/search")
def search_forum():
    return render_template("search_forum.html")

@app.route("/search/results")
def search_results():
    keyword = request.args.get("keyword")
    date_max = request.args.get("date_max")
    date_min = request.args.get("date_min")
    keyword = utilities.sql_like_escape(keyword)
    try:
        date_max = datetime.strptime(date_max, "%Y-%m-%dT%H:%M")
    except:
        date_max = 0
    try:
        date_min = datetime.strptime(date_min, "%Y-%m-%dT%H:%M")
    except:
        date_min = 0
        
    messages = discussion.search_messages(keyword, date_max, date_min)
    threads = discussion.search_threads(keyword, date_max, date_min)
    return render_template("search_results.html", messages=messages, threads=threads)

@app.route("/user/<int:user_id>")
def user_profile(user_id):
    #The user who's profile is being viewed
    user = users.get_user_entry(user_id)
    if not user:
        return render_template("error.html", error_message="Käyttäjää ei löydy")
    #The current clients user_id
    c_user_id = users.user_id()
    #Friend/block relations between the users
    friend_request_sent = users.check_friend(c_user_id, user.id)
    friend_request_received = users.check_friend(user.id, c_user_id)
    user_blocked = users.check_block(c_user_id, user.id)
    blocked_by_user = users.check_block(user.id, c_user_id)
    #Get topics for altering access privileges (admin feature)
    topics = discussion.get_topics_minimal()
    access_rights = users.get_access_rights(user_id)
    restricted_view = not (users.check_admin_role() or (user.public and not users.check_block(user.id, c_user_id)) or (not user.public and friend_request_received))
    return render_template("user_profile.html", user=user, restricted_view=restricted_view, friend_request_sent=friend_request_sent, friend_request_received=friend_request_received, user_blocked=user_blocked, blocked_by_user=blocked_by_user, topics=topics, access_rights=access_rights)

@app.route("/update_access_rights/<int:user_id>", methods=["POST"])
def update_access_rights(user_id):
    if not users.check_admin_role():
        return render_template("error.html", error_message="Ei oikeutta käyttää toimintoa")
    if users.csrf_token() != request.form["csrf_token"]:
            abort(403)
    users.revoke_all_access_rights(user_id)
    accesses = []
    topics = discussion.get_topics_minimal()
    for topic in topics:
        if request.form.get(str(topic.id), "False") == "True":
            accesses.append(topic.id)
    users.grant_access_rights(user_id, accesses)
    return redirect(url_for('user_profile', user_id=user_id))

@app.route("/grant_admin_role/<int:user_id>")
def grant_admin_role(user_id):
    if not users.check_admin_role():
        return render_template("error.html", error_message="Ei oikeutta käyttää toimintoa")
    users.alter_admin_role(user_id, True)
    return redirect(url_for("user_profile", user_id=user_id))

@app.route("/revoke_admin_role/<int:user_id>")
def revoke_admin_role(user_id):
    if not users.check_admin_role():
        return render_template("error.html", error_message="Ei oikeutta käyttää toimintoa")
    users.alter_admin_role(user_id, False)
    return redirect(url_for("user_profile", user_id=user_id))

@app.route("/add_friend/<int:user_id>")
def add_friend(user_id):
    #Current clients user_id
    c_user_id = users.user_id()
    if not c_user_id or c_user_id == user_id or users.check_block(user_id, c_user_id) or users.check_block(c_user_id, user_id):
        return render_template("error.html", error_message="Kaverin lisääminen ei onnistu")
    users.add_friend(c_user_id, user_id)
    return redirect(url_for("user_profile", user_id=user_id))

@app.route("/remove_friend/<int:user_id>")
def remove_friend(user_id):
    users.remove_friend(users.user_id(), user_id)
    return redirect(url_for("user_profile", user_id=user_id))

@app.route("/block/<int:user_id>")
def block_user(user_id):
    #Current clients user_id
    c_user_id = users.user_id()
    if not c_user_id or c_user_id == user_id:
        return render_template("error.html", error_message="Käyttäjän estäminen ei onnistu")
    users.remove_friend(c_user_id, user_id)
    users.add_block(c_user_id, user_id)
    return redirect(url_for("user_profile", user_id=user_id))

@app.route("/unblock/<int:user_id>")
def unblock_user(user_id):
    users.remove_block(users.user_id(), user_id)
    return redirect(url_for("user_profile", user_id=user_id))

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

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("register.html", error_message="Salasanat eivät täsmää", username=username)
        if len(password1) < 1 or len(password1) > 50:
            return render_template("register.html", error_message="Salasanan pituus tulee olla välillä 1-50 merkkiä", username=username)
        if len(username) < 1 or len(username) > 20:
            return render_template("register.html", error_message="Käyttäjätunnuksen pituus tulee olla välillä 1-20 merkkiä")

        if users.register(username, password1):
            return redirect(url_for("index"))
        else:
            return render_template("register.html", error_message="Rekisteröinti epäonnistui. Käyttäjätunnus saattaa olla jo käytössä.")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")