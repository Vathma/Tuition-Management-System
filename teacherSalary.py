import mysql.connector
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import os

# Define the folder where receipts will be saved
SAVE_DIRECTORY = r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\Salary Slips"

# Ensure the directory exists
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

# Database Connection Function
def get_teacher_ids():
    """Fetch distinct Teacher IDs from the class table."""
    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()
        cursor.execute("SELECT DISTINCT teacher_id FROM class")
        teacher_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        db_connection.close()
        return teacher_ids
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

def calculate_teacher_salary(teacher_id, selected_month):
    """Compute base salary and institute fee for a given teacher for a selected month."""
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="rootap",
            password="rootap123",
            database="schooldb"
        )
        cursor = db_connection.cursor(dictionary=True)

        # Step 1: Get all class IDs assigned to the teacher
        query = "SELECT DISTINCT class_id FROM class WHERE teacher_id = %s"
        cursor.execute(query, (teacher_id,))
        class_ids = [row["class_id"] for row in cursor.fetchall()]

        if not class_ids:
            cursor.close()
            db_connection.close()
            return None  # No classes assigned

        # Step 2: Get student-class pairs for attendance (filter by month)
        query = """
        SELECT DISTINCT student_id, class_id 
        FROM attendance 
        WHERE class_id IN (%s) AND MONTH(date) = %s
        """ % (','.join(['%s'] * len(class_ids)), '%s')

        params = class_ids + [selected_month]
        cursor.execute(query, params)
        student_class_mapping = cursor.fetchall()

        if not student_class_mapping:
            cursor.close()
            db_connection.close()
            return None  # No students found for this month

        # Step 3: Calculate base salary based on student payments
        base_salary = 0
        for entry in student_class_mapping:
            student_id, class_id = entry["student_id"], entry["class_id"]

            # Fetch fee amount where student and class match
            query = "SELECT amount FROM fee WHERE student_id = %s AND class_id = %s"
            cursor.execute(query, (student_id, class_id))
            fee_results = cursor.fetchall()  # Fetch all results to avoid unread errors

            for fee in fee_results:
                base_salary += float(fee["amount"])

        # Step 4: Calculate institute fee (20% of base salary)
        institute_fee = base_salary * 0.2

        cursor.close()
        db_connection.close()

        return base_salary, institute_fee

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


# def calculate_teacher_salary(teacher_id, selected_month):
#     """Compute base salary and institute fee for a given teacher for a selected month."""
#     try:
#         db_connection = mysql.connector.connect(
#             host = "localhost",
#             user = "rootap",
#             password = "rootap123",
#             database = "schooldb"
#         )
#         cursor = db_connection.cursor(dictionary=True)

#         # Step 1: Get all class IDs assigned to the teacher
#         query = """
#         SELECT DISTINCT c.class_id
#         FROM class c
#         WHERE c.teacher_id = %s
#         """
#         cursor.execute(query, (teacher_id,))
#         class_ids = [row["class_id"] for row in cursor.fetchall()]

#         if not class_ids:
#             return None  # No classes assigned

#         # Step 2: Get student IDs for each class from attendance table (filter by month)
#         query = """
#         SELECT DISTINCT a.student_id, a.class_id
#         FROM attendance a
#         WHERE a.class_id IN (%s) AND MONTH(a.date) = %s
#         """ % (','.join(['%s'] * len(class_ids)), '%s')

#         params = class_ids + [selected_month]
#         cursor.execute(query, params)
#         student_class_mapping = cursor.fetchall()

#         if not student_class_mapping:
#             return None  # No students found for this month

#         # Step 3: Calculate base salary (sum of all student payments for this teacher's classes)
#         base_salary = 0
#         for entry in student_class_mapping:
#             student_id, class_id = entry["student_id"], entry["class_id"]

#             # Get the fee amount paid by the student
#             query = "SELECT amount FROM fee WHERE student_id = %s"
#             cursor.execute(query, (student_id,))
#             fee_result = cursor.fetchone()

#             if fee_result:
#                 base_salary += float(fee_result["amount"])

#         # Step 4: Calculate institute fee (20% of base salary)
#         institute_fee = base_salary * 0.2

#         cursor.close()
#         db_connection.close()

#         return base_salary, institute_fee

#     except mysql.connector.Error as err:
#         messagebox.showerror("Database Error", f"Error: {err}")
#         return None

# Salary Calculation and Pay Slip Generation
def generate_salary_slip():
    teacher_id = teacher_id_var.get()
    selected_month = month_var.get()
    other_deductions = float(other_deductions_var.get()) if other_deductions_var.get() else 0

    if not teacher_id:
        messagebox.showerror("Input Error", "Please select a Teacher ID!")
        return
    if not selected_month.isdigit() or int(selected_month) not in range(1, 13):
        messagebox.showerror("Input Error", "Please enter a valid month (1-12)!")
        return

    selected_month = int(selected_month)  # Convert month input to integer
    salary_data = calculate_teacher_salary(teacher_id, selected_month)

    if not salary_data:
        messagebox.showerror("Error", "No salary details found for this Teacher ID in the selected month!")
        return

    base_salary, institute_fee = salary_data
    final_salary = base_salary - institute_fee - other_deductions

    # Get current date for salary slip generation date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Generate PDF Pay Slip
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Title
    pdf.cell(200, 10, "TEACHER SALARY PAY SLIP", ln=True, align="C")
    pdf.ln(10)

    # Teacher Salary Details
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Teacher ID: {teacher_id}", ln=True)
    pdf.cell(200, 10, f"Salary Month: {selected_month}", ln=True)
    pdf.cell(200, 10, f"Generated On: {current_date}", ln=True)
    pdf.cell(200, 10, f"Base Salary: Rs. {base_salary:.2f}", ln=True)
    pdf.cell(200, 10, f"Institution Fee (20% of Base): Rs. {institute_fee:.2f}", ln=True)
    pdf.cell(200, 10, f"Other Deductions: Rs. {other_deductions:.2f}", ln=True)
    pdf.cell(200, 10, f"Final Salary Paid: Rs. {final_salary:.2f}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, "Thank you for your service!", ln=True, align="C")

    # Save PDF
    file_path = os.path.join(SAVE_DIRECTORY, f"Salary_Slip_{teacher_id}_{selected_month}.pdf")
    pdf.output(file_path)

    messagebox.showinfo("Success", f"Salary Slip generated: {file_path}")

# GUI Setup
root = tk.Tk()
root.title("Teacher Salary Issuance")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#1ABC9C")

# Title Label
title_label = tk.Label(
        root,
        text="Teacher Salary Issuance",
        font=("Arial", 15, "bold"),
        bg="#1ABC9C",  # Teal color to match the View students theme
        fg="white",
        pady=10
    )
title_label.pack(fill="x")

# Frame for padding
form_frame = tk.Frame(root, bg="#E3F2FD", padx=20, pady=10)
form_frame.pack(pady=10,fill="both", expand=True)

tk.Label(form_frame, text="Select Teacher ID:", bg="#E3F2FD").pack(pady=5)

# Dropdown menu for Teacher IDs
teacher_id_var = tk.StringVar()
teacher_ids = get_teacher_ids()
teacher_id_dropdown = ttk.Combobox(form_frame, textvariable=teacher_id_var, values=teacher_ids, state="readonly", width=28)
teacher_id_dropdown.pack(pady=5)

# Select Month
tk.Label(form_frame, text="Enter Month (1-12):", bg="#E3F2FD").pack(pady=5)
month_var = tk.StringVar()
tk.Entry(form_frame, textvariable=month_var, width=30).pack(pady=5)

# Other Deductions
tk.Label(form_frame, text="Other Deductions:", bg="#E3F2FD").pack(pady=5)
other_deductions_var = tk.StringVar()
tk.Entry(form_frame, textvariable=other_deductions_var, width=30).pack(pady=5)

button_frame = tk.Frame(root, bg="#1ABC9C")
button_frame.pack(pady=10)

# Generate Salary Slip Button
tk.Button(button_frame, text="Generate Salary Slip", command=generate_salary_slip,bg="#E3F2FD").pack(pady=10)

root.mainloop()