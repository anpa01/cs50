import os
import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.jinja_env.filters["usd"] = usd

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT * FROM stocks WHERE user_id = :user",
                          user=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
    total = cash
    stocks = []
    for index, row in enumerate(rows):
        stock_info = lookup(row['symbol'])

        stocks.append(list((stock_info['symbol'], stock_info['name'], row['amount'], stock_info['price'], round(stock_info['price'] * row['amount'], 2))))
        total += stocks[index][4]
    return render_template("index.html", stocks=stocks, cash=round(cash, 2), total=round(total, 2))
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    transacted = datetime.datetime.now()
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        amount = int(request.form.get("amount"))
        stock = lookup(symbol)
        if not stock:
            return apology("Could not find the stock", 400)
        price = lookup(symbol)["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
        cash_after = cash - price * float(amount)
        if cash_after < 0:
            return apology("You don't have enough money", 400)
        stock = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol",
                            user=session["user_id"], symbol=symbol)
        if not stock:
            db.execute("INSERT INTO stocks(user_id, symbol, amount) VALUES (:user, :symbol, :amount)",
                user=session["user_id"], symbol=symbol, amount=amount)
        else:
            amount += stock[0]['amount']

            db.execute("UPDATE stocks SET amount = :amount WHERE user = :user AND symbol = :symbol",
                user=session["user_id"], symbol=symbol, amount=amount)
        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                          cash=cash_after, user=session["user_id"])
        db.execute("INSERT INTO history(user_id, symbol, amount, price, transacted) VALUES(:user_id, :symbol, :amount, :price, :transacted)",
                    user_id=session["user_id"], symbol=symbol, amount=amount, price=price, transacted=transacted)
        flash("Bought!")
        return redirect("/")
@app.route("/history")
@login_required
def history():
    rows = db.execute("SELECT * FROM history WHERE user_id = :user",
                          user=session["user_id"])
    history = []
    for row in rows:
        stock_info = lookup(row['symbol'])
        history.append(list((stock_info['symbol'], row['amount'], row['price'], row['transacted'])))
    return render_template("history.html", history=history)
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == 'GET':
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("Invalid Stock Symbol", 400)
        return render_template("quoted.html", stock=stock)
    return redirect("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("confirmation")
        if password1 != password2:
            return apology("Passwords do not match", 403)
        elif not name:
            return apology("Must provide username", 403)
        elif not password1:
            return apology("Must provide password", 403)
        elif not password2:
            return apology("Must provide confirmation", 403)
        elif db.execute("SELECT * FROM users WHERE username = :name",
                name=name):
            return apology("Username taken", 403)
        db.execute("INSERT INTO users(username, hash) VALUES (:name, :hash)",
            name=name, hash=generate_password_hash(request.form.get("password")))
    return redirect("/")
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    transacted = datetime.datetime.now()
    if request.method == "GET":
        return render_template("sell.html")
    else:
        symbol = request.form.get("symbol")
        amount = int(request.form.get("amount"))
        if not db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol",
                                user=session["user_id"], symbol=symbol):
                return apology("You do not have this many shares", 403)
        placeholder = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol",
                                user=session["user_id"], symbol=symbol)[0]['amount']
        old_amount = placeholder
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
        price = lookup(symbol)['price']
        if amount > old_amount:
            return apology("Too many shares", 403)
        elif amount == old_amount:
            cash_after = cash + price * float(amount)
            db.execute("DELETE FROM stocks WHERE user_id = :user AND symbol = :symbol",
                          symbol=symbol, user=session["user_id"])
            db.execute("INSERT INTO history(user_id, symbol, amount, price, transacted) VALUES(:user_id, :symbol, :amount, :price, :transacted)",
                    user_id=session["user_id"], symbol=symbol, amount=amount * -1, price=price, transacted=transacted)
            db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                          cash=cash_after, user=session["user_id"])
        else:
            new_amount = old_amount - amount
            cash_after = cash + price * float(amount)
            db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user AND symbol = :symbol",
                          symbol=symbol, user=session["user_id"], amount = new_amount)
            db.execute("INSERT INTO history(user_id, symbol, amount, price, transacted) VALUES(:user_id, :symbol, :amount, :price, :transacted)",
                    user_id=session["user_id"], symbol=symbol, amount=amount * -1, price=price, transacted=transacted)
            db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                          cash=cash_after, user=session["user_id"])
    flash("Sold!")
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
            return apology("Passwords aren't same", 403)
        elif not oldpassword:
            return apology("must provide password", 403)
        elif not newpassword:
            return apology("must provide new password", 403)
        elif not newpasswordconfirm:
            return apology("must confirm new password", 403)
        elif not name:
            return apology("must provide username", 403)
        elif len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("incorrect username or password", 403)
        else:
            db.execute("UPDATE users SET hash = :hash WHERE id = :user",
                        hash=generate_password_hash(request.form.get("new_password")), user=session["user_id"])
        flash("Password Changed!")
        return redirect("/")
def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)