from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from config import DATABASE, SECRET_KEY
from datetime import datetime

app = Flask(__name__)
app.secret_key = SECRET_KEY


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO users(fullname,email,password) VALUES(?,?,?)",
            (fullname, email, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    total = conn.execute(
        """
        SELECT IFNULL(SUM(amount),0)
        FROM expenses
        WHERE user_id=?
        """,
        (session["user_id"],)
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        fullname=session["fullname"],
        total=total
    )


@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        category = request.form["category"]
        amount = request.form["amount"]
        payment_method = request.form["payment_method"]
        expense_date = request.form["expense_date"]
        notes = request.form["notes"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO expenses
            (user_id,category,amount,payment_method,expense_date,notes)
            VALUES(?,?,?,?,?,?)
            """,
            (
                session["user_id"],
                category,
                amount,
                payment_method,
                expense_date,
                notes
            )
        )

        conn.commit()
        conn.close()

        return redirect("/expenses")

    today = datetime.today().strftime("%Y-%m-%d")

    return render_template(
        "add_expense.html",
        today=today
    )
@app.route("/expenses")
def view_expenses():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    expenses = conn.execute(
        """
        SELECT *
        FROM expenses
        WHERE user_id=?
        ORDER BY expense_date DESC
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "expenses.html",
        expenses=expenses
    )


@app.route("/edit_expense/<int:id>", methods=["GET", "POST"])
def edit_expense(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    if request.method == "POST":

        category = request.form["category"]
        amount = request.form["amount"]
        payment_method = request.form["payment_method"]
        expense_date = request.form["expense_date"]
        notes = request.form["notes"]

        conn.execute(
            """
            UPDATE expenses
            SET category=?,
                amount=?,
                payment_method=?,
                expense_date=?,
                notes=?
            WHERE id=? AND user_id=?
            """,
            (
                category,
                amount,
                payment_method,
                expense_date,
                notes,
                id,
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        return redirect("/expenses")

    expense = conn.execute(
        """
        SELECT *
        FROM expenses
        WHERE id=? AND user_id=?
        """,
        (id, session["user_id"])
    ).fetchone()

    conn.close()

    return render_template(
        "edit_expense.html",
        expense=expense
    )


@app.route("/delete_expense/<int:id>")
def delete_expense(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM expenses
        WHERE id=? AND user_id=?
        """,
        (id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/expenses")


if __name__ == "__main__":
    app.run(debug=True)