from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_FILE = "users.db"

# Create database if it doesn't exist
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    error = ""
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username")
        password = request.form.get("password")

        if action == "signup":
            success = add_user(username, password)
            if success:
                return redirect(url_for("panel"))
            else:
                error = "Username already exists!"
        elif action == "login":
            user = get_user(username)
            if user and user[2] == password:
                return redirect(url_for("panel"))
            else:
                error = "Wrong username or password!"

    return render_template("index.html", error=error)

@app.route("/panel")
def panel():
    return render_template("panel.html")

if __name__ == "__main__":
    app.run(debug=True)
