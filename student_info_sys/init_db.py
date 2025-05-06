import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Zukaata_1245'
)
c = conn.cursor()

# Create database if not exists
c.execute("CREATE DATABASE IF NOT EXISTS student_info_db")
c.execute("USE student_info_db")

# Drop tables to reset mock data (optional in dev only)
c.execute("DROP TABLE IF EXISTS registrations")
c.execute("DROP TABLE IF EXISTS attendance")
c.execute("DROP TABLE IF EXISTS grades")
c.execute("DROP TABLE IF EXISTS courses")
c.execute("DROP TABLE IF EXISTS faculty")

# Create tables
c.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    faculty_id INT,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS grades (
    student_id INT,
    course_id INT,
    grade VARCHAR(5),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    student_id INT,
    course_id INT,
    percentage FLOAT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS notices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT,
    target VARCHAR(255)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    message TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS support (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_type VARCHAR(50),
    user_id INT,
    message TEXT
)
""")

# Insert mock faculty
mock_faculty = [
    ("Prof. A. Sharma", "a.sharma@college.edu", "password"),
    ("Dr. Meera Nair", "m.nair@college.edu", "password"),
    ("Mr. R. Singh", "r.singh@college.edu", "password"),
    ("Ms. T. Das", "t.das@college.edu", "password"),
    ("Dr. John Doe", "john.doe@example.com", "password"),
]
c.executemany("INSERT INTO faculty (name, email, password) VALUES (%s, %s, %s)", mock_faculty)

# Insert mock courses (faculty_id assumes order from above)
mock_courses = [
    ("Data Structures", 1),
    ("Operating Systems", 2),
    ("Database Management Systems", 3),
    ("Web Technologies", 4),
    ("Software Engineering", 1),
    ("Computer Networks", 2),
    ("Artificial Intelligence", 5),
    ("Machine Learning", 5),
]
c.executemany("INSERT INTO courses (title, faculty_id) VALUES (%s, %s)", mock_courses)

# Finalize
conn.commit()
conn.close()
