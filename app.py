from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "college_smart_portal_secret"


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():
    conn = sqlite3.connect("myproject.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# CREATE DATABASE TABLES
# =========================

def init_db():

    conn = get_db_connection()

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Students table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT UNIQUE NOT NULL,
            branch TEXT NOT NULL,
            attendance INTEGER NOT NULL,
            marks INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================
# HOME
# =========================

@app.route("/")
def home():

    conn = get_db_connection()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "home.html",
        total_students=total_students
    )

# =========================
# NOTICE BOARD
# =========================

@app.route("/notice")
def notice():
    return render_template("notice.html")
# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        try:

            conn.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
                """,
                (username, email, password)
            )

            conn.commit()

            flash(
                "Registration successful! Please login.",
                "success"
            )

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            flash(
                "Username or email already exists.",
                "danger"
            )

        finally:

            conn.close()

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter email and password.", "danger")
            return render_template("login.html")

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT * FROM users
            WHERE email = ? AND password = ?
            """,
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash("Login successful!", "success")

            return redirect(url_for("home"))

        else:

            flash("Invalid email or password.", "danger")

    return render_template("login.html")

# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(url_for("login"))


# =========================
# RECORDS
# =========================

@app.route("/records")
def records():

    search = request.args.get("search", "").strip()
    branch = request.args.get("branch", "").strip()
    attendance = request.args.get("attendance", "").strip()

    conn = get_db_connection()

    query = """
        SELECT * FROM students
        WHERE 1=1
    """

    params = []

    # Search by name, roll or branch
    if search:

        query += """
            AND (
                name LIKE ?
                OR roll LIKE ?
                OR branch LIKE ?
            )
        """

        params.extend([
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ])

    # Branch filter
    if branch:

        query += " AND branch = ?"

        params.append(branch)

    # Attendance filter
    if attendance:

        query += " AND attendance = ?"

        params.append(attendance)

    query += " ORDER BY id DESC"

    students = conn.execute(
        query,
        params
    ).fetchall()

    conn.close()

    return render_template(
        "record.html",
        students=students,
        search=search
    )


# =========================
# ADD STUDENT
# =========================

@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"].strip()
        roll = request.form["roll"].strip()
        branch = request.form["branch"].strip()

        attendance = request.form["attendance"].strip()
        marks = request.form["marks"].strip()

        # Convert attendance and marks to integers
        try:

            attendance = int(attendance)
            marks = int(marks)

        except ValueError:

            flash(
                "Attendance and marks must be numbers.",
                "danger"
            )

            return redirect(url_for("add_student"))

        conn = get_db_connection()

        try:

            conn.execute(
                """
                INSERT INTO students
                (name, roll, branch, attendance, marks)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name,
                    roll,
                    branch,
                    attendance,
                    marks
                )
            )

            conn.commit()

            flash(
                "Student added successfully!",
                "success"
            )

            return redirect(url_for("records"))

        except sqlite3.IntegrityError:

            flash(
                "Roll number already exists.",
                "danger"
            )

        finally:

            conn.close()

    return render_template("add_student.html")


# =========================
# STUDENT DETAILS
# =========================

@app.route("/student/<int:id>")
def student_details(id):

    conn = get_db_connection()

    student = conn.execute(
        """
        SELECT * FROM students
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    conn.close()

    if student is None:

        return "Student not found", 404

    return render_template(
        "student_details.html",
        student=student
    )


# =========================
# DELETE STUDENT
# =========================

@app.route("/delete_student/<int:id>")
def delete_student(id):

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM students
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    flash(
        "Student deleted successfully.",
        "success"
    )

    return redirect(url_for("records"))


# =========================
# ABOUT
# =========================

@app.route("/about")
def about():

    return render_template("about.html")


# =========================
# 404 ERROR PAGE
# =========================

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)