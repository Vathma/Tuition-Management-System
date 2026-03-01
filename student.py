import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="rootap",
        password="rootap123",
        database="schooldb"
    )

# Function to generate the next student number
def get_next_student_no():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(student_id) FROM student")
    max_student_no = cursor.fetchone()[0]
    conn.close()

    if max_student_no:  # If there is already a student number
        next_no = int(max_student_no[1:]) + 1
        return f"s{str(next_no).zfill(4)}"
    else:  # If no student number exists, start with s0001
        return "s0001"

def add_student(name, grade, email, dob, address, phone_no):
    conn = connect()
    cursor = conn.cursor()

    # Generate the next student number
    student_no = get_next_student_no()

    # Insert the new student into the table
    cursor.execute(
        "INSERT INTO student (student_id, name, grade, email, dob, address, phone_no,user_id) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",
        (student_no, name, grade, email, dob, address, phone_no,2)
    )
    conn.commit()
    conn.close()

def fetch_students():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    conn.close()
    return students
