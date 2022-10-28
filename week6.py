# coding=UTF-8
from flask import Flask, request, render_template, session, redirect
import mysql.connector
import os # for secret key

#create connection
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "an890147",
    database = "website"
)
cursor = mydb.cursor(dictionary=True)

# create application object
app = Flask(
    __name__,
    static_folder = "static",
    static_url_path = "/"
)

# create the secret key (generate random string)
app.secret_key = os.urandom(20)

# Request-1
# homepage
@app.route("/")
def home():
    return render_template("homepage.html")

# Request-2
# for creating an account
@app.route("/signup", methods = ["POST"])
def signup():
    # get name, username, password from form by POST
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    # check if username exists or not using MySQL
    cursor.execute("SELECT * FROM member WHERE username=%s LIMIT 1", (username,))
    check_exist = cursor.fetchone()
    if check_exist is None:
        return redirect("/error?message=帳號已經被註冊")
    else:
        # create membet in table "member"
        cursor.execute("INSERT INTO member(name, username, password) VALUES(%s, %s, %s)", (name, username, password,))
        mydb.commit()
        return redirect("/")
    
# Request-3
# sign in
@app.route("/signin", methods = ["POST"])
def signin():
    # get username, password from form by POST
    username = request.form.get("username")
    password = request.form.get("password")
    cursor.execute("SELECT * FROM member WHERE username=%s AND password=%s", (username, password,))
    member = cursor.fetchone()
    if member:
        # create session
        session["id"] = member[0]
        session["name"] = member[1]
        session["username"] = member[2]
        return redirect("/member")
    else:
        return redirect("/error?message=帳號或密碼輸入錯誤")

# Request-4
# /signout
@app.route("/signout")
def signout():
    session.pop("username")
    return redirect("/")

# /member
@app.route("/member")
def member():
    # if user has signed in
    if "username" in session:
        return render_template ("member.html", name = session["name"])

# /error
@app.route("/error")
def error():
    # get query string of message
    message = request.args.get("message")
    # show message on error page
    return render_template("error.html", message = message)

# /back
@app.route("/back")
def back():
    return redirect("/")

app.run(port = 3000)