from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Create an in-memory SQLite database
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'securepassword')")
conn.commit()

@app.route('/')
def vulnerable():
    username = request.args.get("username", "")

    # 🚨 Vulnerable SQL Query (SQL Injection)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        return f"Welcome {user[1]}!"
    else:
        return "User not found."

if __name__ == '__main__':
    app.run(debug=True)
