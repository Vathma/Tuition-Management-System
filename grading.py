# grading.py
import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="rootap",
        password="rootap123",
        database="schooldb"
    )

def view_student_grades(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT test_id, subject_id, marks 
        FROM studentmark 
        WHERE student_id=%s
    """, (student_id,))
    grades = cursor.fetchall()
    conn.close()
    return grades

def get_student_marks_by_teacher(teacher_id):
    """Retrieve student marks for subjects assigned to the given teacher."""
    conn = connect()
    cursor = conn.cursor()
    query = """
        SELECT DISTINCT sm.test_id, sm.student_id, sm.subject_id, sm.marks
        FROM studentmark sm
        JOIN class c ON sm.subject_id = c.subject_id
        WHERE c.teacher_id = %s
    """
    cursor.execute(query, (teacher_id,))
    marks = cursor.fetchall()
    conn.close()
    return marks

def add_student_marks(test_id, subject_id, student_id, marks):
    """Insert a new student mark into the studentmark table."""
    conn = connect()
    cursor = conn.cursor()
    query = """
        INSERT INTO studentmark (test_id, subject_id ,student_id, marks)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (test_id, subject_id, student_id, marks))
    conn.commit()
    conn.close()

def update_student_marks(test_id, subject_id, student_id, new_marks):
    """Update student marks in the database."""
    conn = connect()
    cursor = conn.cursor()
    query = """
        UPDATE studentmark
        SET marks = %s
        WHERE test_id = %s AND student_id = %s AND subject_id = %s
    """
    cursor.execute(query, (new_marks, test_id, student_id, subject_id))
    conn.commit()
    conn.close()