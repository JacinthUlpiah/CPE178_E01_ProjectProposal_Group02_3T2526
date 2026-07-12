from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "AI_SPENDING_2026"

DATABASE = "spending.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        income = request.form["income"]

        conn = get_db_connection()

        existing = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if existing:
            conn.close()
            return "Email already exists."

        conn.execute(
            """
            INSERT INTO users
            (fullname,email,password,monthly_income)
            VALUES(?,?,?,?)
            """,
            (fullname, email, password, income)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]

            return redirect(url_for("dashboard"))

        return "Invalid email or password."

    return render_template("login.html")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        fullname=session["fullname"]
    )


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)