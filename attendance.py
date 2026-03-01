# attendance.py
import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="rootap",
        password="rootap123",
        database="schooldb"
    )

def mark_attendance(student_id, class_id, attendance_status, date):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attendance (student_id, class_id, attendance_status, date) 
        VALUES (%s, %s, %s, %s)
    """, (student_id, class_id, attendance_status, date))
    conn.commit()
    conn.close()

def view_student_attendance(student_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, class_id, attendance_status 
        FROM attendance 
        WHERE student_id=%s
    """, (student_id,))
    attendance_records = cursor.fetchall()
    conn.close()
    return attendance_records
