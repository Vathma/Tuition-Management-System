import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

# Database connection function
def get_class_ids(student_id):
    if not student_id:
        return []
    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()
        cursor.execute("SELECT class_id FROM studentclass WHERE student_id = %s", (student_id,))  # Fetch all class IDs
        class_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        db_connection.close()
        return class_ids
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

# Function to update the class ID dropdown based on student ID input
def update_class_id_dropdown(*args):
    student_id = student_id_var.get().strip()
    class_id_dropdown["values"] = get_class_ids(student_id)

# Function to update fee in the database
def update_fee():
    student_id = student_id_var.get().strip()
    class_id = class_id_var.get().strip()
    amount = amount_var.get().strip()
    due_date = due_date_var.get()
    # paid = paid_var.get()

    if not student_id or not amount or not class_id:
        messagebox.showwarning("Input Error", "Please enter Student ID, Class ID, and Amount!")
        return

    try:
        db_connection = mysql.connector.connect(
            host = "localhost",
            user = "rootap",
            password = "rootap123",
            database = "schooldb"
        )
        cursor = db_connection.cursor()

        # Insert fee details into the fee table
        query = """
        INSERT INTO fee (student_id, class_id, amount, due_date, paid) 
        VALUES (%s, %s, %s, %s, 1)
        """
        cursor.execute(query, (student_id, class_id, amount, due_date))

        db_connection.commit()
        cursor.close()
        db_connection.close()

        messagebox.showinfo("Success", "Fee added successfully!")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# GUI Setup
root = tk.Tk()
root.title("Update Class Fees")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#1ABC9C")

# Title Label
title_label = tk.Label(
        root,
        text="Update Class Fees",
        font=("Arial", 15, "bold"),
        bg="#1ABC9C",  # Teal color to match the View students theme
        fg="white",
        pady=10
    )
title_label.pack(fill="x")

# Frame for padding
form_frame = tk.Frame(root, bg="#E3F2FD", padx=20, pady=10)
form_frame.pack(pady=10,fill="both", expand=True)

# Student ID
tk.Label(form_frame, text="Student ID:", bg="#E3F2FD").pack(pady=5)
student_id_var = tk.StringVar()
tk.Entry(form_frame, textvariable=student_id_var, width=30).pack(pady=5)

# Class ID (Dropdown)
tk.Label(form_frame, text="Class ID:", bg="#E3F2FD").pack(pady=5)
class_id_var = tk.StringVar()
class_id_dropdown = ttk.Combobox(form_frame, textvariable=class_id_var, state="readonly", width=28)
class_id_dropdown.pack(pady=5)

# Bind event to update class IDs when student ID is changed
student_id_var.trace_add("write", update_class_id_dropdown)

# Amount
tk.Label(form_frame, text="Amount (Rs.):", bg="#E3F2FD").pack(pady=5)
amount_var = tk.StringVar()
tk.Entry(form_frame, textvariable=amount_var, width=30).pack(pady=5)

# Due Date (Calendar)
tk.Label(form_frame, text="Due Date:", bg="#E3F2FD").pack(pady=5)
due_date_var = DateEntry(form_frame, width=18, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
due_date_var.pack(pady=5)

# # Paid (Yes/No)
# tk.Label(form_frame, text="Paid:", bg="#E3F2FD").pack(pady=5)
# paid_var = tk.IntVar(value=0)
# tk.Radiobutton(form_frame, text="Yes", variable=paid_var, value=1).pack()
# tk.Radiobutton(form_frame, text="No", variable=paid_var, value=0).pack()

button_frame = tk.Frame(root, bg="#1ABC9C")
button_frame.pack(pady=10)

# Update Button
tk.Button(button_frame, text="Update Fee", command=update_fee,bg="#E3F2FD").pack(pady=10)

root.mainloop()
