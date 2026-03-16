# login.py
import sys
import os
from PIL import Image, ImageTk

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
sys.path.append(os.path.dirname(current_dir))

import tkinter as tk
from tkinter import messagebox
# import sqlite3
import mysql.connector

def connect():

    return mysql.connector.connect(
    host = "localhost",
    user = "rootap",
    password = "rootap123",
    database = "schooldb"
)
    # db_cursor =conn.cursor()

from gui.admin_dashboard import AdminDashboard
from gui.teacher_dashboard import TeacherDashboard
from gui.student_dashboard import StudentDashboard


# Function to validate user login
def validate_login(username, password, role):
    conn = connect()
    cursor = conn.cursor()

    # Check user credentials in the users table
    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s AND role = %s", (username, password, role))
    result = cursor.fetchone()
    conn.close()
    
    return result

# Additional function to get teacher_id or student_id if different
def get_role_specific_id(username, role):
    conn = connect()
    cursor = conn.cursor()
    
    specific_id = None  # Default to None
    
    if role == "teacher":
        cursor.execute("SELECT teacher_id FROM teacher WHERE user_id = (SELECT user_id FROM user WHERE username = %s)", (username,))
        result = cursor.fetchone()
        specific_id = result[0] if result else None

    elif role == "student":
        cursor.execute("SELECT student_id FROM student WHERE user_id = (SELECT user_id FROM user WHERE username = %s)", (username,))
        result = cursor.fetchone()
        specific_id = result[0] if result else None

    conn.close()
    return specific_id  # Return correct ID

# Function to update the password
def change_password(username, old_password, new_password):
    conn = connect()
    cursor = conn.cursor()

    # Check if the old password is correct
    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, old_password))
    user = cursor.fetchone()

    if user:
        # Update the password
        cursor.execute("UPDATE user SET password = %s WHERE username = %s", (new_password, username))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

# Function to launch the appropriate dashboard
def launch_dashboard(role, user_id=None):
    if role == "admin":
        admin_dashboard = AdminDashboard()
        admin_dashboard.mainloop()
    elif role == "teacher":
        teacher_dashboard = TeacherDashboard(user_id)
        teacher_dashboard.mainloop()
    elif role == "student":
        student_dashboard = StudentDashboard(user_id)
        student_dashboard.mainloop()
    else:
        messagebox.showerror("Invalid Role", "An unexpected role was encountered.")

# Change Password Window
class ChangePasswordWindow(tk.Toplevel):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title("Change Password")
        self.geometry("400x350")
        self.resizable(False, False)
        self.configure(bg="#1ABC9C")

        # Title Label
        title_label = tk.Label(
                self,
                text="Change Password",
                font=("Arial", 15, "bold"),
                bg="#1ABC9C",  # Teal color to match the View students theme
                fg="white",
                pady=10
            )
        title_label.pack(fill="x")

        # Frame for padding
        form_frame = tk.Frame(self, bg="#E3F2FD", padx=20, pady=10)
        form_frame.pack(pady=10,fill="both", expand=True)

        tk.Label(form_frame, text="Current Password:", bg="#E3F2FD").pack(pady=5)
        self.old_password_entry = tk.Entry(form_frame, show="*")
        self.old_password_entry.pack(pady=5)

        tk.Label(form_frame, text="New Password:", bg="#E3F2FD").pack(pady=5)
        self.new_password_entry = tk.Entry(form_frame, show="*")
        self.new_password_entry.pack(pady=5)

        tk.Label(form_frame, text="Confirm New Password:", bg="#E3F2FD").pack(pady=5)
        self.confirm_password_entry = tk.Entry(form_frame, show="*")
        self.confirm_password_entry.pack(pady=5)

        button_frame = tk.Frame(self, bg="#1ABC9C")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Change Password", command=self.change_password,bg="#E3F2FD").pack(pady=10)

    def change_password(self):
        old_password = self.old_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not old_password or not new_password or not confirm_password:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        if new_password != confirm_password:
            messagebox.showwarning("Input Error", "New passwords do not match!")
            return

        if change_password(self.username, old_password, new_password):
            messagebox.showinfo("Success", "Password changed successfully!")
            self.destroy()
        else:
            messagebox.showerror("Error", "Current password is incorrect!")

# Login window
class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("800x500")
        self.resizable(False, False)

        # Load and display background image
        self.bg_image = Image.open(r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\images\background.png") 
        self.bg_image = self.bg_image.resize((800, 500), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self, width=800, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Get canvas size dynamically
        canvas_width = 800
        canvas_height = 500
        form_x = canvas_width // 2  # Center horizontally
        form_y = canvas_height // 3  # Adjust slightly above center

        # Store the form position
        self.form_x = form_x
        self.form_y = form_y

        # Create login form elements on the canvas
        self.create_widgets()

    def create_widgets(self):
    # Title (Use a slightly darker white for contrast)
        self.canvas.create_text(self.form_x, self.form_y - 80, text="Tuition Management System", font=("Arial", 14, "bold"), fill="#1A3E5A")  # Dark blue

        # Username Label
        self.canvas.create_text(self.form_x - 80, self.form_y - 40, text="Username:", anchor="e",font=("Arial", 10, "bold"), fill="#134857")  # Dark teal
        self.username_entry = tk.Entry(self)
        self.username_window = self.canvas.create_window(self.form_x + 20, self.form_y - 40, window=self.username_entry, width=150)

        # Password Label
        self.canvas.create_text(self.form_x - 80, self.form_y, text="Password:", anchor="e",font=("Arial", 10, "bold"), fill="#134857")  # Dark teal
        self.password_entry = tk.Entry(self, show="*")
        self.password_window = self.canvas.create_window(self.form_x + 20, self.form_y, window=self.password_entry, width=150)

        # Role Dropdown
        self.canvas.create_text(self.form_x - 80, self.form_y + 40, text="Role:", anchor="e",font=("Arial", 10, "bold"), fill="#134857")  # Dark teal
        self.role_var = tk.StringVar(value="admin")
        self.role_dropdown = tk.OptionMenu(self, self.role_var, "admin", "teacher", "student")
        self.role_dropdown_window = self.canvas.create_window(self.form_x + 20, self.form_y + 40, window=self.role_dropdown, width=150)

        # Login Button
        self.login_button = tk.Button(self, text="Login", bg="#1A3E5A", fg="white", command=self.login)
        self.change_button = tk.Button(self,text="Change Password",bg="#1ABC9C", fg="white", command=self.open_change_password_window)
        # self.login_button_window = self.canvas.create_window(200, 230, window=self.login_button, width=100)
        self.login_button_window = self.canvas.create_window(self.form_x, self.form_y + 80, window=self.login_button, width=100)
        self.change_button_window = self.canvas.create_window(self.form_x, self.form_y + 120, window=self.change_button, width=120)



    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get().strip()

        # Validate login and get user details
        user = validate_login(username, password, role)

        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {role.capitalize()}!")

            self.destroy()
            # Launch the dashboard in a separate function
            launch_dashboard(role, user[0] if role in ("teacher", "student") else None)
        else:
            messagebox.showerror("Login Failed", "Invalid username, password, or role!")
    
    def open_change_password_window(self):
        username = self.username_entry.get().strip()
        if username:
            ChangePasswordWindow(username)
        else:
            messagebox.showwarning("Input Error", "Please enter your username first!")

# Run the login app
if __name__ == "__main__":
  app = LoginApp()
  app.mainloop()
