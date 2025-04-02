from flask import Flask, request, jsonify, render_template
import mysql.connector
from werkzeug.security import check_password_hash

app = Flask(__name__)

# MySQL Database Connection (XAMPP)
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Leave empty if no password is set in XAMPP
    "database": "user_db"
}

# Route: Login Page
@app.route('/')
def login_page():
    return render_template('index.html')

# Route: Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            return jsonify({"success": True, "redirect": "/dashboard"}), 200
        else:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401

    except mysql.connector.Error as err:
        return jsonify({"success": False, "error": f"Database Error: {err}"}), 500

# Route: Dashboard (After Login)
@app.route('/dashboard')
def dashboard():
    return "<h1>Welcome to the Dashboard!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
