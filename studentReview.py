import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Function to fetch teacher IDs from the teacher table
def fetch_teacher_ids():
    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()

        cursor.execute("SELECT teacher_id FROM teacher")
        teachers = cursor.fetchall()

        cursor.close()
        db_connection.close()

        return [str(teacher[0]) for teacher in teachers]

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

# Function to fetch subject ID based on selected teacher ID
def fetch_subject_id(teacher_id):
    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()

        query = "SELECT subject_id FROM teacher WHERE teacher_id = %s"
        cursor.execute(query, (teacher_id,))
        result = cursor.fetchone()

        cursor.close()
        db_connection.close()

        return result[0] if result else "N/A"

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return "N/A"

# Function to update subject ID when teacher ID is selected
def update_subject_id(*args):
    teacher_id = teacher_id_var.get()
    if teacher_id:
        subject_id = fetch_subject_id(teacher_id)
        subject_id_var.set(subject_id)

# Function to insert review data into the database
def insert_review():
    student_id = student_id_var.get().strip()
    teacher_id = teacher_id_var.get().strip()
    subject_id = subject_id_var.get().strip()
    review_text = review_text_var.get("1.0", tk.END).strip()
    review_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Auto-updated date

    if not student_id or not teacher_id or not review_text:
        messagebox.showwarning("Input Error", "Please fill all required fields!")
        return

    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()

        # Insert review data into the database
        query = "INSERT INTO review (student_id, teacher_id, subject_id, review_text, date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (student_id, teacher_id, subject_id, review_text, review_date))

        db_connection.commit()
        cursor.close()
        db_connection.close()

        messagebox.showinfo("Success", "Review added successfully!")
        student_id_var.set("")
        review_text_var.delete("1.0", tk.END)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# GUI Setup
root = tk.Tk()
root.title("Student Review Form")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#1ABC9C")

# Title Label
title_label = tk.Label(
        root,
        text="Student Review Form",
        font=("Arial", 15, "bold"),
        bg="#1ABC9C",  # Teal color to match the View students theme
        fg="white",
        pady=10
    )
title_label.pack(fill="x")

# Frame for padding
form_frame = tk.Frame(root, bg="#E3F2FD", padx=20, pady=10)
form_frame.pack(pady=10,fill="both", expand=True)

# Student ID Input
tk.Label(form_frame, text="Student ID:", bg="#E3F2FD").pack(pady=5)
student_id_var = tk.StringVar()
tk.Entry(form_frame, textvariable=student_id_var, width=30).pack(pady=5)

# Teacher ID Dropdown
tk.Label(form_frame, text="Teacher ID:", bg="#E3F2FD").pack(pady=5)
teacher_id_var = tk.StringVar()
teacher_dropdown = ttk.Combobox(form_frame, textvariable=teacher_id_var, values=fetch_teacher_ids(), state="readonly", width=28)
teacher_dropdown.pack(pady=5)
teacher_id_var.trace("w", update_subject_id)  # Update subject_id when teacher_id changes

# Subject ID (Auto-filled)
tk.Label(form_frame, text="Subject ID (Auto-filled):", bg="#E3F2FD").pack(pady=5)
subject_id_var = tk.StringVar()
subject_entry = tk.Entry(form_frame, textvariable=subject_id_var, state="readonly", width=30)
subject_entry.pack(pady=5)

# Review Text Input
tk.Label(form_frame, text="Review:", bg="#E3F2FD").pack(pady=5)
review_text_var = tk.Text(form_frame, height=5, width=40)
review_text_var.pack(pady=5)

button_frame = tk.Frame(root, bg="#1ABC9C")
button_frame.pack(pady=10)

# Submit Button
tk.Button(button_frame, text="Submit Review", command=insert_review,bg="#E3F2FD").pack(pady=10)

root.mainloop()
