import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
import datetime
import os

# Define the folder where receipts will be saved
SAVE_DIRECTORY = r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\Review Reports"

# Ensure the directory exists
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

# Function to fetch student IDs from the database
def fetch_student_ids():
    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()

        cursor.execute("SELECT DISTINCT student_id FROM studentmark")
        students = cursor.fetchall()

        cursor.close()
        db_connection.close()

        return [str(student[0]) for student in students]

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

# Function to fetch teacher names
def get_teacher_name(teacher_id):
    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()

        cursor.execute("SELECT name FROM teacher WHERE teacher_id = %s", (teacher_id,))
        result = cursor.fetchone()

        cursor.close()
        db_connection.close()

        return result[0] if result else teacher_id  # Return teacher name or ID if not found

    except mysql.connector.Error:
        return teacher_id  # Return ID if any error occurs

# Function to fetch subject names
def get_subject_name(subject_id):
    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()

        cursor.execute("SELECT name FROM subject WHERE subject_id = %s", (subject_id,))
        result = cursor.fetchone()

        cursor.close()
        db_connection.close()

        return result[0] if result else subject_id  # Return subject name or ID if not found

    except mysql.connector.Error:
        return subject_id  # Return ID if any error occurs

# Function to fetch student marks and reviews
def fetch_student_data(student_id):
    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()

        # Fetch student marks
        cursor.execute("SELECT test_id, subject_id, marks FROM studentmark WHERE student_id = %s", (student_id,))
        marks_data = cursor.fetchall()

        # Fetch student reviews
        cursor.execute("SELECT teacher_id, subject_id, review_text, date FROM review WHERE student_id = %s", (student_id,))
        reviews_data = cursor.fetchall()

        cursor.close()
        db_connection.close()

        return marks_data, reviews_data

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return [], []

# Function to generate a PDF report
def generate_pdf():
    student_id = student_id_var.get().strip()

    if not student_id:
        messagebox.showwarning("Input Error", "Please select a Student ID!")
        return

    marks_data, reviews_data = fetch_student_data(student_id)

    if not marks_data and not reviews_data:
        messagebox.showinfo("No Data", "No marks or reviews found for this student.")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Title
    pdf.cell(200, 10, f"Student Report - {student_id}", ln=True, align="C")
    pdf.ln(10)

    # Add date
    report_date = datetime.datetime.now().strftime("%Y-%m-%d")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Generated on: {report_date}", ln=True, align="C")
    pdf.ln(10)

    # Marks Table
    if marks_data:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Marks Report", ln=True, align="L")
        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(60, 10, "Test ID", 1, 0, "C")
        pdf.cell(80, 10, "Subject Name", 1, 0, "C")
        pdf.cell(50, 10, "Marks", 1, 1, "C")

        pdf.set_font("Arial", "", 12)
        for row in marks_data:
            subject_name = get_subject_name(row[1])  # Get subject name
            pdf.cell(60, 10, str(row[0]), 1, 0, "C")
            pdf.cell(80, 10, subject_name, 1, 0, "C")
            pdf.cell(50, 10, str(row[2]), 1, 1, "C")

        pdf.ln(10)

  # Reviews Table
    if reviews_data:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Reviews", ln=True, align="L")
        pdf.ln(5)

        # Table Header (All in One Line)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(50, 10, "Teacher Name", 1, 0, "C")
        pdf.cell(50, 10, "Subject Name", 1, 0, "C")
        pdf.cell(30, 10, "Date", 1, 0, "C")
        pdf.cell(60, 10, "Review", 1, 1, "C")  # Move to next row

        # Table Data (All in One Line)
        pdf.set_font("Arial", "", 10)
        for row in reviews_data:
            teacher_name = get_teacher_name(row[0])  # Get teacher name
            subject_name = get_subject_name(row[1])  # Get subject name

            pdf.cell(50, 10, teacher_name, 1, 0, "C")
            pdf.cell(50, 10, subject_name, 1, 0, "C")
            pdf.cell(30, 10, str(row[3]), 1, 0, "C")  # Date
            pdf.cell(60, 10, str(row[2]), 1, 1, "C")  # Review

        pdf.ln(10)  # Space after the table

    # Save PDF
    # pdf_filename = f"Student_Report_{student_id}.pdf"
    # pdf.output(pdf_filename)
    file_path = os.path.join(SAVE_DIRECTORY, f"Student_Report_{student_id}.pdf")
    pdf.output(file_path)
    
    messagebox.showinfo("Success", f"PDF Generated: {file_path}")

# GUI Setup
root = tk.Tk()
root.title("Generate Student Report")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#1ABC9C")

# Title Label
title_label = tk.Label(
        root,
        text="Generate Student Report",
        font=("Arial", 15, "bold"),
        bg="#1ABC9C",  # Teal color to match the View students theme
        fg="white",
        pady=10
    )
title_label.pack(fill="x")

# Frame for padding
form_frame = tk.Frame(root, bg="#E3F2FD", padx=20, pady=10)
form_frame.pack(pady=10,fill="both", expand=True)


# Student ID Selection
tk.Label(form_frame, text="Select Student ID:", bg="#E3F2FD").pack(pady=5)
student_id_var = tk.StringVar()
student_dropdown = ttk.Combobox(form_frame, textvariable=student_id_var, values=fetch_student_ids(), state="readonly")
student_dropdown.pack(pady=5)

button_frame = tk.Frame(root, bg="#1ABC9C")
button_frame.pack(pady=10)

# Generate Report Button
tk.Button(button_frame, text="Generate Report", command=generate_pdf, bg="#E3F2FD").pack(pady=10)

root.mainloop()
