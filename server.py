from flask import Flask, render_template, abort, request, redirect, session, jsonify
from client import User, Mission, Post
import database
import sqlite3
import os

app = Flask (__name__)
user = None
ranks = {0: "Peasant", 1: "Soldier", 95: "Sniper", 96: "Brainy Intelligence", 97: "Second Commander", 98: "Cheif Advisor", 99: "First Commander", 100: "Lord"}
UPLOAD_FOLDER = "/static/upload"
ALLOWED_EXTENSIONS = set (["png", "jpg", "jpeg", "gif"])
#app.secret_key = "12345"

@app.route ("/")
def index ():
    #uid = session.get ("my_uid")
    with database.connect () as conn:
        database.initTable (conn)
        global user
        #user = database.getUser (conn, "admin")
    return render_template ("index.html", tab = "index", user = user)

def allowedFile (filename):
    return filename.rsplit (".", 1) [1].lower () in ALLOWED_EXTENSIONS

@app.route ("/posts", methods = ["GET", "POST"])
def posts ():

    global user

    if request.method == "POST":
        print ("LMAO")
        title = request.form.get ("title")
        text = request.form.get ("text")

        print (title)
        print (text)

        if "file" not in request.files:
            print ("NO FILE")
            return redirect (request.url)
        file = request.files ["file"]
        if file.filename == "":
            return redirect (request.url)
        print (file)

        path = os.path.dirname (__file__) + "/static/upload" + user.username

        if not os.path.exists (path):
            os.makedirs (path)
        if file and allowedFile (file.filename):
            filename = file.filename
            file.save (path, filename)

        return jsonify (title, text, file)

    # with database.connect () as conn:    
    #     posts = database.getAllPosts (conn)

    return render_template ("posts.html", tab = "posts", user = user)

@app.route ("/login", methods = ["GET", "POST"])
def login ():
    username = ""
    errors = {}
    global user
    if request.method == "POST":
        username = request.form.get ("username").strip ()
        if not username:
            errors ["username"] = "enter username"

        password = request.form.get ("password").strip ()
        if not password:
            errors ["password"] = "enter password"

        if len (errors) == 0:
            with database.connect () as conn:
                tmp = database.login (conn, username, password)
                if tmp == -1:
                    errors ["username"] = username + " does not exist"
                elif tmp == -2:
                    errors ["password"] = "wrong password"
                else:
                    user = User (tmp [0][0], tmp [0][1], tmp [0][2], tmp [0][3])
                    print ("Successfully Logged In!")
                    return redirect ("/")
    
    return render_template ("login.html", username = username, errors = errors, tab = "login", user = user)

@app.route ("/signup", methods = ["GET", "POST"])
def signup ():
    username = ""
    displayName =  ""
    errors = {}
    global user
    if request.method == "POST":
        with database.connect () as conn:
            username = request.form.get ("username")
            if not username:
                errors ["username"] = "enter a username"
            elif len (username.split ()) > 1 or username != username.strip ():
                errors ["username"] = "spaces are not allowed in username"
            elif not database.unique (conn, "username", username):
                errors ["username"] = username + " has been taken"

            displayName = request.form.get ("displayName")
            if not displayName:
                errors ["displayName"] = "enter a display name"
            elif displayName != displayName.strip ():
                errors ["displayName"] = "display name cannot start or end with spaces"
            elif not database.unique (conn, "displayName", displayName):
                errors ["displayName"] = displayName + " has been taken"

            password = request.form.get ("password")
            if not password:
                errors ["password"] = "enter a password"
            elif len (password.split ()) > 1 or password != password.strip ():
                errors ["password"] = "spaces are not allowed in password"

            confirmPassword = request.form.get ("confirmPassword")
            if not confirmPassword:
                errors ["confirmPassword"] = "confirm password"
            elif password != None and password != confirmPassword:
                errors ["confirmPassword"] = "passwords do not match"

            if len (errors) == 0:
                user = User (username, displayName, password, 0)
                database.addUser (conn, user)
                return redirect ("/")

    return render_template ("signup.html", username = username, displayName = displayName, errors = errors, tab = "signup", user = user)

@app.route ("/myaccount")
def myAccount ():
    global user
    return render_template ("myaccount.html", tab = "myaccount", user = user)

@app.route ("/mymissions", methods = ["GET", "POST"])
def myMissions ():
    order = request.args.get ("order")

    if request.method == "POST":
        x = request.form.get ("name")
        y = request.form.get ("description")
        z = request.form.get ("rank")
        w = request.form.get ("reward")
        mission = Mission (None, x, y, z, w)
        with database.connect () as conn:
            database.addMission (conn, mission)
        return jsonify ((x, y, z, w))

    with database.connect () as conn:
        missions = database.getAllMissions (conn, "All", order)

    if order == "name":
        order = "Name"
    elif order == "rank":
        order = "Rank"
    elif order == "reward":
        order = "Reward"
    
    global user
    return render_template ("mymissions.html", missions = missions, order = order, tab = "mymissions", user = user)

@app.route ("/store")
def store ():
    global user
    return render_template ("store.html", tab = "store", user = user)

@app.route ("/contact")
def contact ():
    global user
    return render_template ("contact.html", tab = "contact", user = user)

@app.route ("/manage", methods = ["GET", "POST"])
def manage ():
    order = request.args.get ("order")

    if request.method == "POST":
        x = request.form.get ("username")
        y = request.form.get ("displayName")
        z = request.form.get ("password")
        w = request.form.get ("rank")
        with database.connect () as conn:
            database.updateUser (conn, x, y, z, w)
        return jsonify ((x, y, z, w))

    with database.connect () as conn:
        users = database.getAllUsers (conn, order)

    if order == "username":
        order = "Username"
    elif order == "displayName":
        order = "Display name"
    elif order == "password":
        order == "Password"
    elif order == "rank":
        order = "Rank"
    
    global user
    global ranks
    return render_template ("manage.html", users = users, order = order, ranks = ranks, tab = "manage", user = user)

@app.route ("/deleteUser/<username>")
def deleteUser (username):
    with database.connect () as conn:
        database.deleteUser (conn, username)
    return redirect ("/manage")


@app.route ("/deleteMission/<name>")
def deleteMission (name):
    with database.connect () as conn:
        database.deleteMission (conn, name)
    return redirect ("/mymissions")

@app.route ("/logout")
def logout ():
    print ("Log Out!")
    #session ["my_uid"] = None
    global user
    user = None
    return redirect ("/")