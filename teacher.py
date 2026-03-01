import mysql.connector
from tkinter import messagebox

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="rootap",
        password="rootap123",
        database="schooldb"
    )

# Function to generate the next teacher number
def get_next_teacher_no():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(teacher_id) FROM teacher")
    max_teacher_no = cursor.fetchone()[0]
    conn.close()

    if max_teacher_no:  # If there is already a teacher number
        next_no = int(max_teacher_no[1:]) + 1
        return f"t{str(next_no).zfill(3)}"
    else:  # If no teacher number exists, start with t001
        return "t001"

def add_teacher(name, email, phone_no, subject_id,user_id):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Generate the next teacher number
        teacher_no = get_next_teacher_no()

        # Insert the new teacher into the table
        cursor.execute(
            "INSERT INTO teacher (teacher_id, name, email, phone_no, subject_id,user_id) VALUES (%s, %s, %s, %s, %s,%s)",
            (teacher_no, name, email, phone_no, subject_id,user_id)
        )

        conn.commit()
        messagebox.showinfo("Success", "Teacher added successfully")
    except mysql.connector.Error as err:
        conn.rollback()  # Rollback in case of error
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
    
    conn.close()

def fetch_teachers():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teacher")
    teachers = cursor.fetchall()
    conn.close()
    return teachers
