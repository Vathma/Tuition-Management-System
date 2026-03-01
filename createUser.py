import mysql.connector
import tkinter as tk
from tkinter import messagebox

def connect():
    """Connects to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="rootap",
        password="rootap123",
        database="schooldb"
    )

def get_next_number(role_prefix):
    """Finds the next available number for the given role (teacher/student)."""
    conn = connect()
    cursor = conn.cursor()
    query = f"SELECT username FROM user WHERE username LIKE '{role_prefix}%' ORDER BY user_id DESC LIMIT 1"
    cursor.execute(query)
    last_user = cursor.fetchone()
    conn.close()

    if last_user:
        last_number = int(last_user[0][len(role_prefix):])  # Extract the number from username
        return last_number + 1
    return 1  # Start from 1 if no existing users

def create_user(role):
    """Creates a new teacher or student user."""
    role_prefix = "teacher" if role == "teacher" else "student"
    next_no = get_next_number(role_prefix)
    username = f"{role_prefix}{next_no}"
    password = f"{role[0]}{next_no}pass"  # Example: t1pass, s2pass

    # Insert into database
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (username, password, role) VALUES (%s, %s, %s)", 
                   (username, password, role))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"User Created!\nUsername: {username}\nPassword: {password}")

# GUI for Creating User
root = tk.Tk()
create_window = tk.Toplevel(root)
create_window.title("Create User Account")
create_window.geometry("500x400")
create_window.resizable(False, False)
create_window.configure(bg="#1ABC9C")

# Title Label
title_label = tk.Label(
        create_window,
        text="Create User Account",
        font=("Arial", 15, "bold"),
        bg="#1ABC9C",  # Teal color to match the View students theme
        fg="white",
        pady=10
    )
title_label.pack(fill="x")

# Frame for padding
form_frame = tk.Frame(create_window, bg="#E3F2FD", padx=20, pady=8)
form_frame.pack(pady=10,fill="both", expand=True)

tk.Label(form_frame, text="Select Role:", font=("Arial", 12, "bold"), bg="#E3F2FD", fg="#1ABC9C").pack(pady=10)

tk.Button(form_frame, text="Create Teacher", command=lambda: create_user("teacher"), bg="#3498DB", fg="white", font=("Arial", 10)).pack(pady=5)
tk.Button(form_frame, text="Create Student", command=lambda: create_user("student"), bg="#2ECC71", fg="white", font=("Arial", 10)).pack(pady=5)

def close_window():
    create_window.destroy()  # Close the create user window
    root.destroy()

button_frame = tk.Frame(create_window, bg="#1ABC9C")
button_frame.pack(pady=10)
tk.Button(button_frame, text="Close", command=close_window, bg="red", fg="white").pack(pady=10)


root.withdraw()

create_window.mainloop()
    