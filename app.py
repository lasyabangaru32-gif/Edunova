from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "edunova_secret_key"

import os

load_dotenv()

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

APP_NAME = "EduNova"
APP_VERSION = "1.0"

# ---------------- HOME ----------------
@app.route('/')
def index():
    return render_template('index.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == "admin@edunova.com" and password == "12345":
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid credentials"

    return render_template('login.html', error=error)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM courses")
    total_courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assignments")
    total_assignments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assignments WHERE status='pending'")
    pending_assignments = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 5")
    recent_students = cursor.fetchall()

    db.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_courses=total_courses,
        total_assignments=total_assignments,
        pending_assignments=pending_assignments,
        recent_students=recent_students
    )
# ======================================================
# STUDENTS MODULE (MYSQL)
# ======================================================
@app.route('/students', methods=['GET', 'POST'])
def students():

    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        course = request.form.get('course')

        cursor.execute(
            "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
            (name, age, course)
        )
        db.commit()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    db.close()

    return render_template('students.html', students=data)
# ======================================================
# DELETE STUDENT ROUTE
# ======================================================

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
    db.commit()

    db.close()

    return redirect(url_for('students'))



# ======================================================
# EDIT / UPDATE STUDENT ROUTE
# ======================================================
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM students WHERE id=%s", (student_id,))
    student = cursor.fetchone()

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        course = request.form.get('course')

        cursor.execute("""
            UPDATE students
            SET name=%s, age=%s, course=%s
            WHERE id=%s
        """, (name, age, course, student_id))

        db.commit()
        db.close()
        return redirect(url_for('students'))

    db.close()
    return render_template('edit_student.html', student=student)

# ======================================================
# COURSES MODULE
# ======================================================
@app.route('/courses', methods=['GET', 'POST'])
def courses():

    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_code = request.form.get('course_code')
        instructor = request.form.get('instructor')

        cursor.execute(
            "INSERT INTO courses (course_name, course_code, instructor) VALUES (%s, %s, %s)",
            (course_name, course_code, instructor)
        )
        db.commit()

    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()

    db.close()

    return render_template('courses.html', courses=data)
# ======================================================
# DELETE COURSE ROUTE
# ======================================================

@app.route('/delete_course/<int:course_id>')
def delete_course(course_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM courses WHERE id=%s", (course_id,))
    db.commit()

    db.close()

    return redirect(url_for('courses'))


# ======================================================
# EDIT COURSE ROUTE
# ======================================================

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM courses WHERE id=%s", (course_id,))
    course = cursor.fetchone()

    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_code = request.form.get('course_code')
        instructor = request.form.get('instructor')

        cursor.execute("""
            UPDATE courses
            SET course_name=%s, course_code=%s, instructor=%s
            WHERE id=%s
        """, (course_name, course_code, instructor, course_id))

        db.commit()
        db.close()
        return redirect(url_for('courses'))

    db.close()
    return render_template('edit_course.html', course=course)
# ======================================================
# ASSIGNMENTS MODULE
# ======================================================

@app.route('/assignments', methods=['GET', 'POST'])
def assignments():

    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        status = request.form.get('status')

        cursor.execute(
            "INSERT INTO assignments (title, due_date, status) VALUES (%s, %s, %s)",
            (title, due_date, status)
        )
        db.commit()

    cursor.execute("SELECT * FROM assignments")
    data = cursor.fetchall()

    db.close()

    return render_template('assignments.html', assignments=data)
# ======================================================
# DELETE ASSIGNMENT ROUTE
# ======================================================
@app.route('/delete_assignment/<int:assignment_id>')
def delete_assignment(assignment_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM assignments WHERE id=%s", (assignment_id,))
    db.commit()

    db.close()

    return redirect(url_for('assignments'))


# ======================================================
# EDIT ASSIGNMENT ROUTE
# ======================================================
@app.route('/edit_assignment/<int:assignment_id>', methods=['GET', 'POST'])
def edit_assignment(assignment_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM assignments WHERE id=%s", (assignment_id,))
    assignment = cursor.fetchone()

    if request.method == 'POST':
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        status = request.form.get('status')

        cursor.execute("""
            UPDATE assignments
            SET title=%s, due_date=%s, status=%s
            WHERE id=%s
        """, (title, due_date, status, assignment_id))

        db.commit()
        db.close()
        return redirect(url_for('assignments'))

    db.close()
    return render_template('edit_assignment.html', assignment=assignment)

# ======================================================
# SETTINGS PAGE
# ======================================================

@app.route('/settings')
def settings():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('settings.html')

@app.route('/about')
def about():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('about.html')


@app.route('/help')
def help():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('help.html')


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 