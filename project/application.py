import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///library.db")

@app.route("/")
@login_required
def index():
    libraries = []
    rows = db.execute("SELECT * FROM books WHERE id = :user",
                    user=session["user_id"])
    nowpage = 0
    for row in rows:
        if not row['currentpage']:
            db.execute("UPDATE books SET currentpage = :currentpage WHERE id = :user AND name = :name",
                    currentpage=nowpage, user=session["user_id"], name=row['name'])
        libraries.append(list((row['name'], row['author'], row['pages'], round(((row['currentpage'] * 100)/ row['pages']), 2))))
    return render_template("index.html", libraries = libraries)
#row['name'], row['author'], row['pages'], ((row['currentpage'] * 100)/ row['pages'])
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        x = True
        y = True
        while x:
            if not request.form.get("username"):
                flash("Must put in username.")
            else:
                x = False
        while y:
            if not request.form.get("password"):
                flash("Must put in password")
            else:
                y = False
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Login is incorrect. Please try again.")
            return redirect("/login")
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")
@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")
    flash("Successfully logged out!")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("password2")
        email = request.form.get("email")
    if not name:
        flash("Must provide username.")
        return redirect("/register")
    elif not password1:
        flash("Must provide password.")
        return redirect("/register")
    elif not password2:
        flash("Must provide confirmation.")
        return redirect("/register")
    elif password1 != password2:
        flash("Passwords don't match.")
        return redirect("/register")
    elif not email:
        flash("Enter your email")
        return redirect("/register")
    elif db.execute("SELECT * FROM users WHERE username = :name",
            name=name):
        flash("Username has been taken.")
        return redirect("/register")
    else:
        db.execute("INSERT INTO users(username, hash, email) VALUES (:name, :hash, :email)",
            name=name, hash=generate_password_hash(request.form.get("password")), email=request.form.get("email"))
        return redirect("/login")
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        name = request.form.get("book")
        author = request.form.get("author")
        pages = request.form.get("pages")
        if not name:
            flash("Please type in the name of the book.")
            return redirect("/")
        elif not author:
            flash("Please type in the name of the author.")
            return redirect("/")
        elif not pages:
            flash("Please type in the number of pages in the book.")
            return redirect("/")
        elif not db.execute("SELECT name FROM books WHERE id = :user AND name = :name",
                        user=session["user_id"], name=name):
            db.execute("INSERT INTO books(id, name, author, pages) VALUES(:user_id, :name, :author, :pages)",
                    user_id=session["user_id"], name=name, author=author, pages=pages)
        else:
            flash("You already have this book.")
            return redirect("/")
        flash("Added!")
        return redirect("/update")
@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "GET":
        books = []
        rows = db.execute("SELECT * FROM books WHERE id = :user",
                    user=session["user_id"])
        if not (db.execute("SELECT name FROM books WHERE id = :user",
                            user=session["user_id"])):
            flash("You can't delete any books.")
            return redirect("/")
        for row in rows:
            books.append((row['name']))
        return render_template("delete.html", books=books)
    else:
        book = request.form.get("book")
        db.execute("DELETE FROM books WHERE id = :user AND name = :book",
                    user=session["user_id"], book=book)
        flash("Deleted!")
        return redirect("/")
@app.route("/history")
@login_required
def history():
    libraries = []
    rows = db.execute("SELECT * FROM history WHERE id = :user",
                    user=session["user_id"])
    for row in rows:
        libraries.append(list((row['name'], row['author'], row['pages'])))
    return render_template("history.html", libraries=libraries)
@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "GET":
        books = []
        rows = db.execute("SELECT * FROM books WHERE id = :user",
                    user=session["user_id"])
        if not (db.execute("SELECT name FROM books WHERE id = :user",
                            user=session["user_id"])):
            flash("You can't update any books.")
            return redirect("/")
        for row in rows:
            books.append((row['name']))
        return render_template("update.html", books=books)
    else:
        currentpage = int(request.form.get("pages"))
        book = request.form.get("book")
        author = db.execute("SELECT author FROM books WHERE name = :book",
                            book=book)[0]['author']
        pages = db.execute("SELECT pages FROM books WHERE name = :book",
                            book=book)[0]['pages']
        if currentpage > pages:
            currentpage = 0
            db.execute("UPDATE books SET currentpage = :currentpage WHERE id = :user AND name = :book",
                        currentpage=currentpage, user=session["user_id"], book=book)
            flash("Automatically Set to 0.")
            return redirect("/")
        elif currentpage == pages:
            db.execute("INSERT INTO history(name, author, pages, id) VALUES(:book, :author, :pages, :user)",
                        book=book, author=author, pages=pages, user=session["user_id"])
            db.execute("DELETE FROM books WHERE name = :book",
                        book=book)
        db.execute("UPDATE books SET currentpage = :currentpage WHERE id = :user AND name = :book",
                    currentpage=currentpage, user=session["user_id"], book=book)
        flash("Updated!")
        return redirect("/")
@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    if request.method == "GET":
        return render_template("changepassword.html")
    else:
        name = request.form.get("username")
        oldpassword = request.form.get("old_password")
        newpassword = request.form.get("new_password")
        newpasswordconfirm = request.form.get("new_password1")
        rows = db.execute("SELECT * FROM users WHERE username = :name",
                          name=name)
        if newpassword != newpasswordconfirm:
            flash("Passwords aren't the same")
            return redirect("/changepassword")
        elif not oldpassword:
            flash("Must type in old password")
            return redirect("/changepassword")
        elif not newpassword:
            flash("Must type in new password.")
            return redirect("/changepassword")
        elif not newpasswordconfirm:
            flash("Must confirm password")
            return redirect("/changepassword")
        elif not name:
            flash("Must type in name")
            return redirect("/changepassword")
        elif len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            flash("Username or Password is incorrect")
            return redirect("/changepassword")
        else:
            db.execute("UPDATE users SET hash = :hash WHERE id = :user",
                        hash=generate_password_hash(request.form.get("new_password")), user=session["user_id"])
        flash("Password Changed!")
        return redirect("/")
@app.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
    if request.method == "GET":
        return render_template("forgotpassword.html")
    else:
        user = request.form.get("user")
        email = request.form.get("email")
        if not db.execute("SELECT * FROM users WHERE username = :user",
                                user=user):
            flash("Username doesn't exist")
            return redirect("/forgotpassword")
        originalemail = db.execute("SELECT email FROM users WHERE username = :user",
                                    user=user)[0]["email"]
        if originalemail == email:
            return redirect("/forgotpassword2")
        else:
            flash("Incorrect email.")
            return redirect("/login")
@app.route("/forgotpassword2", methods=["GET", "POST"])
def forgotpassword2():
    if request.method == "GET":
        return render_template("forgotpassword2.html")
    else:
        user = request.form.get("user")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        hash = generate_password_hash(request.form.get("password"))
        if password != password2:
            flash("Passwords aren't same.")
            return redirect("/forgotpassword2")
        elif not db.execute("SELECT * FROM users WHERE username = :user",
                                user=user):
            flash("Username doesn't exist")
            return redirect("/forgotpassword2")
        else:
            db.execute("UPDATE users SET hash = :hash WHERE username = :user",
                        hash=generate_password_hash(request.form.get("password")), user=user)
        flash("Password Changed!")
        return redirect("/login")