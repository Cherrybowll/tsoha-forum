from app import app
from flask import redirect, render_template, request
import users


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/placeholder")
def placeholder():
    pass

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