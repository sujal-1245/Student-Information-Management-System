import mysql.connector
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'secret'

# Database connection function
def get_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Zukaata_1245',  # Use your MySQL password
        database='student_info_db'  # Use the existing database
    )
    return conn

# Route to render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to student profile page
@app.route('/profile_student')
def profile_student():
    return render_template('profile_student.html')


@app.route('/register_courses')
def register_courses():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT courses.id, courses.title, faculty.name AS faculty_name 
        FROM courses 
        LEFT JOIN faculty ON courses.faculty_id = faculty.id
    """)
    courses = cursor.fetchall()
    return render_template('register_courses.html', courses=courses)

# Route to view student grades
@app.route('/grades')
def grades():
    return render_template('grades.html')

# Route to view student attendance
@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

# Route to view student notices
@app.route('/notices')
def notices():
    return render_template('notices.html')

# Route for student feedback
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Route for student support
@app.route('/support')
def support():
    return render_template('support.html')

# Route to view faculty courses
@app.route('/faculty_courses')
def faculty_courses():
    return render_template('faculty_courses.html')

# Route for faculty to upload grades
@app.route('/upload_grades')
def upload_grades():
    return render_template('upload_grades.html')

# Route for faculty to manage attendance
@app.route('/manage_attendance')
def manage_attendance():
    return render_template('manage_attendance.html')

# Route for faculty to view notices
@app.route('/faculty_notices')
def faculty_notices():
    return render_template('faculty_notices.html')

# Route for faculty to view student reports
@app.route('/student_reports')
def student_reports():
    return render_template('student_reports.html')

# Route for faculty support
@app.route('/faculty_support')
def faculty_support():
    return render_template('faculty_support.html')

# Route for student login
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(dictionary=True)  # Fetch rows as dictionaries
        cursor.execute("SELECT * FROM students WHERE email=%s AND password=%s", (email, password))
        student = cursor.fetchone()
        if student:
            session['user'] = dict(student)
            session['role'] = 'student'
            return redirect('/student_dashboard')
        else:
            return "Invalid credentials"
    return render_template('student_login.html')

# Route for faculty login
@app.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(dictionary=True)  # Fetch rows as dictionaries
        cursor.execute("SELECT * FROM faculty WHERE email=%s AND password=%s", (email, password))
        faculty = cursor.fetchone()
        if faculty:
            session['user'] = dict(faculty)
            session['role'] = 'faculty'
            return redirect('/faculty_dashboard')
        else:
            return "Invalid credentials"
    return render_template('faculty_login.html')

@app.route('/student_dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect('/')
    
    db = get_db()
    student_id = session['user']['id']
    cursor = db.cursor(dictionary=True)  # Fetch rows as dictionaries

    # Fetch all courses (assuming student is auto-enrolled in all)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    # Fetch grades for the student
    cursor.execute("SELECT * FROM grades WHERE student_id=%s", (student_id,))
    grades = cursor.fetchall()

    # Fake progress data for each course
    courses_progress = [
        {"title": "Data Structures", "percentage": 85},
        {"title": "Operating Systems", "percentage": 75},
        {"title": "DBMS", "percentage": 90},
        {"title": "Web Technologies", "percentage": 80},
        {"title": "Machine Learning", "percentage": 60},
        {"title": "Artificial Intelligence", "percentage": 70},
        {"title": "Software Engineering", "percentage": 95}
    ]

    # Fetch notices for the student
    cursor.execute("SELECT * FROM notices WHERE target='student'")
    notices = cursor.fetchall()

    cursor.close()
    
    return render_template(
        'student_dashboard.html',
        courses=courses,
        grades=grades,
        courses_progress=courses_progress,
        notices=notices
    )

# Route for faculty dashboard (after login)
@app.route('/faculty_dashboard')
def faculty_dashboard():
    if session.get('role') != 'faculty':
        return redirect('/')
    db = get_db()
    faculty_id = session['user']['id']
    cursor = db.cursor(dictionary=True)  # Fetch rows as dictionaries
    cursor.execute("SELECT * FROM courses WHERE faculty_id=%s", (faculty_id,))
    courses = cursor.fetchall()

    cursor.execute("SELECT * FROM notices WHERE target='faculty'")
    notices = cursor.fetchall()

    return render_template('faculty_dashboard.html', courses=courses, notices=notices)

# Route for student registration
@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        # Check if the email already exists in the students table
        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        existing_student = cursor.fetchone()

        if existing_student:
            # If the email already exists, return an error message
            return render_template('student_register.html', error="Email already in use.")

        # Insert the new student into the database
        cursor.execute("INSERT INTO students (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()

        # Get the student_id of the newly registered student
        cursor.execute("SELECT id FROM students WHERE email = %s", (email,))
        student_id = cursor.fetchone()['id']

        # Insert mock attendance data for all courses
        mock_attendance = [
            (student_id, 1, 85),  # 1st course, 85% attendance
            (student_id, 2, 75),  # 2nd course, 75% attendance
            (student_id, 3, 90),  # 3rd course, 90% attendance
            (student_id, 4, 80),  # 4th course, 80% attendance
            (student_id, 5, 70),  # 5th course, 70% attendance
            (student_id, 6, 95),  # 6th course, 95% attendance
            (student_id, 7, 88),  # 7th course, 88% attendance
            (student_id, 8, 92)   # 8th course, 92% attendance
        ]
        cursor.executemany("INSERT INTO attendance (student_id, course_id, percentage) VALUES (%s, %s, %s)", mock_attendance)
        db.commit()

        return redirect('/student_login')  # Redirect to student login after successful registration

    return render_template('student_register.html')



# Route for faculty registration
@app.route('/register_faculty', methods=['GET', 'POST'])
def register_faculty():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Insert the new faculty into the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO faculty (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()

        return redirect('/faculty_login')  # Redirect to faculty login after successful registration

    return render_template('faculty_register.html')


# Route for student logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
