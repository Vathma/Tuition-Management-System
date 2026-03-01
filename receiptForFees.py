# pip install mysql-connector-python reportlab tkcalendar
#generate fee receipt
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import os

# Define the folder where receipts will be saved
SAVE_DIRECTORY = r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\Fee Receipts"

# Ensure the directory exists
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

# Function to generate PDF receipt
def generate_receipt():
    student_id = student_id_var.get().strip()
    selected_month = month_var.get()

    if not student_id or not selected_month:
        messagebox.showwarning("Input Error", "Please select Student ID and Month!")
        return

    try:
        # Database connection
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()

        # Convert month name to month number
        month_number = datetime.datetime.strptime(selected_month, "%B").month

        # Fetch all PAID fees for the student in the selected month
        query = """
            SELECT class_id, due_date, amount 
            FROM fee 
            WHERE student_id = %s 
            AND MONTH(due_date) = %s 
            AND paid = 1
        """
        cursor.execute(query, (student_id, month_number))
        fees = cursor.fetchall()

        cursor.close()
        db_connection.close()

        if not fees:
            messagebox.showinfo("No Data", "No paid fees found for this student in the selected month.")
            return

        # PDF file name
        # pdf_filename = f"Fee_Receipt_{student_id}_{selected_month}.pdf"
        # Save PDF in the specified directory
        file_path = os.path.join(SAVE_DIRECTORY, f"Fee_Receipt_{student_id}_{selected_month}.pdf")


        # Create PDF
        c = canvas.Canvas(file_path, pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 800, "Fee Payment Receipt")

        # Student details
        c.setFont("Helvetica", 12)
        c.drawString(50, 770, f"Student ID: {student_id}")
        c.drawString(50, 750, f"Month: {selected_month}")

        # Generate date
        generated_date = datetime.datetime.now().strftime("%Y-%m-%d")
        c.drawString(50, 730, f"Generated on: {generated_date}")

        # Table headers
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 670, "Class ID")
        c.drawString(150, 670, "Due Date")
        c.drawString(280, 670, "Amount (Rs.)")
        c.line(50, 665, 400, 665)

        # Table content
        y_position = 640
        c.setFont("Helvetica", 12)
        total_amount = 0

        for fee in fees:
            class_id, due_date, amount = fee[0], fee[1], fee[2]
            total_amount += amount

            c.drawString(50, y_position, str(class_id))  # Class ID
            c.drawString(150, y_position, str(due_date))  # Due Date
            c.drawString(280, y_position, f"Rs. {amount:.2f}")  # Amount
            y_position -= 20

        # Total amount
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position - 20, f"Total Amount Paid: Rs. {total_amount:.2f}")

        # Save and close PDF
        c.save()
        messagebox.showinfo("Success", f"Receipt generated successfully: {file_path}")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

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

        query = "SELECT DISTINCT student_id FROM fee"
        cursor.execute(query)
        students = cursor.fetchall()

        cursor.close()
        db_connection.close()

        return [str(student[0]) for student in students]

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

# GUI Setup
root = tk.Tk()
root.title("Generate Fee Receipt")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#1ABC9C")

# Title Label
title_label = tk.Label(
        root,
        text="Generate Fee Receipt",
        font=("Arial", 15, "bold"),
        bg="#1ABC9C",  # Teal color to match the View students theme
        fg="white",
        pady=10
    )
title_label.pack(fill="x")

# Frame for padding
form_frame = tk.Frame(root, bg="#E3F2FD", padx=20, pady=10)
form_frame.pack(pady=10,fill="both", expand=True)

# Student ID Dropdown
tk.Label(form_frame, text="Select Student ID:", bg="#E3F2FD").pack(pady=5)
student_id_var = tk.StringVar()
student_dropdown = ttk.Combobox(form_frame, textvariable=student_id_var, values=fetch_student_ids(), width=30)
student_dropdown.pack(pady=5)

# Month Dropdown
tk.Label(form_frame, text="Select Month:", bg="#E3F2FD").pack(pady=5)
month_var = tk.StringVar()
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_dropdown = ttk.Combobox(form_frame, textvariable=month_var, values=months, state="readonly", width=28)
month_dropdown.pack(pady=5)

button_frame = tk.Frame(root, bg="#1ABC9C")
button_frame.pack(pady=10)

# Generate Button
tk.Button(button_frame, text="Generate Receipt", command=generate_receipt,bg="#E3F2FD").pack(pady=10)

root.mainloop()
