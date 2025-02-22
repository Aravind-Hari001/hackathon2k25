from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt  # Ensure you have bcrypt installed
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "secret-key"

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Myprem@2003kumar"
app.config["MYSQL_DB"] = "user_system"

mysql = MySQL(app)


@app.route("/", methods=["GET", "POST"])
def login():
    errors = []  # Initialize errors list outside try block

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # Check if email or password is empty
        if not email:
            errors.append("Please enter your email.")
        if not password:
            errors.append("Please enter your password.")

        if errors:
            return render_template("login.html", errors=errors)

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            users = cursor.fetchone()
            cursor.close()

            if users and users["password"]== password:
                session["loggedin"] = True
                session["email"] = users["email"]
                return redirect(url_for("dashboard"))
            else:
                errors.append("Invalid Email or Password. Please try again!")

        except Exception as e:
            errors.append(f"Database error: {str(e)}")

    return render_template("login.html", errors=errors)


@app.route("/dashboard")
def dashboard():
    if "loggedin" in session:
        return render_template("dashboard.html", email=session["email"])
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/check_db")
def check_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        return f"Connected to database: {db_name}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
