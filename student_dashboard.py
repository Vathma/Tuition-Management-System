# student_dashboard.py
import tkinter as tk
import subprocess
from PIL import Image, ImageTk
import os
import sys
# # Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(current_dir)
# Add the parent directory to the system path
sys.path.append(os.path.dirname(current_dir))
from modules.grading import view_student_grades
from modules.attendance import view_student_attendance
from modules.viewFees import view_student_fee
from tkinter import ttk, messagebox
import mysql.connector

class StudentDashboard(tk.Tk):
    def __init__(self, user_id,student_id=None):
        super().__init__()
        self.user_id = user_id
        self.student_id = self.get_student_id()  # Retrieve student ID

        self.title("Student Dashboard")
        self.geometry("800x700")
        self.resizable(False, False)
        self.configure(bg="#1ABC9C")  # Match theme

        if not self.student_id:
            tk.Label(self, text="Error: Student ID not found", fg="red", bg="#1ABC9C").pack()
            return

        def logout():
            """Logout and redirect to the login page."""
            self.destroy()
            subprocess.Popen(["python", os.path.join(main_dir, "gui/login.py")])

        # Title Label
        tk.Label(self, text="Student Dashboard", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

        # Frame for Icons and Buttons
        btn_frame = tk.Frame(self, bg="#1ABC9C")
        btn_frame.pack(pady=20)

        # Button Details (icon path, text, command)
        buttons = [
            ("images/viewMarks.png", "View Grades", self.show_grades),
            ("images/viewAttendance.png", "View Attendance", self.show_attendance),
            ("images/viewReviews.png", "View Reviews", self.view_reviews),
            ("images/viewFees.png", "View Fees", self.show_fee)
        ]

        # Load and display buttons with icons
        for i, (icon_path, text, command) in enumerate(buttons):
            full_path = os.path.join(main_dir, icon_path)  # Get full path for images
            img = Image.open(full_path).resize((80, 80), Image.LANCZOS)  
            img = ImageTk.PhotoImage(img)

            col = i % 2  # Two columns
            row = i // 2  # New row every 2 items

            # Icon
            label = tk.Label(btn_frame, image=img, bg="#1ABC9C")
            label.image = img  # Keep reference
            label.grid(row=row * 2, column=col, padx=20, pady=10)

            # Button (Updated color to `#F39C12`)
            btn = tk.Button(
                btn_frame, text=text, command=command,
                bg="#F39C12", fg="white", font=("Arial", 12, "bold"), width=20
            )
            btn.grid(row=(row * 2) + 1, column=col, padx=20, pady=5)

        logout_button = tk.Button(self, text="Logout", command=logout, bg="red", fg="white", font=("Arial", 12))
        logout_button.pack(side="bottom", pady=10)

        # Frame to hold dynamic tables
        self.table_frame = tk.Frame(self, bg="#1ABC9C")
        self.table_frame.pack(pady=20)

        self.grades_tree = None  # Placeholder for grades table
        self.attendance_tree = None  # Placeholder for attendance table

    def get_student_id(self):
        """Fetch student ID from user ID."""
        conn = mysql.connector.connect(host="localhost", user="rootap", password="rootap123", database="schooldb")
        cursor = conn.cursor()
        cursor.execute("SELECT student_id FROM student WHERE user_id = %s", (self.user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def create_icon_button(self, frame, icon_key, text, command, row, col):
        """Creates a button with an icon above it."""
        icon_label = tk.Label(frame, image=self.icons[icon_key], bg="#2C3E50")
        icon_label.grid(row=row * 2, column=col, padx=20, pady=5)

        btn = tk.Button(frame, text=text, command=command, bg="#F39C12", fg="white", font=("Arial", 12), width=20)
        btn.grid(row=(row * 2) + 1, column=col, padx=20, pady=5)

    def load_icon(self, path, size=(80, 80)):
        """Loads and resizes an image."""
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def create_table(self, columns):
        """Create and return a TreeView table dynamically."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()  # Clear previous tables

        tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(pady=10)

        return tree

    def show_grades(self):
        """Fetch and display grades dynamically."""
        grades = view_student_grades(self.student_id)

        if not grades:
            messagebox.showinfo("Grades", "No grades available.")
            return

        self.grades_tree = self.create_table(["Test ID", "Subject ID", "Marks"])
        self.update_table(self.grades_tree, grades)

    def show_attendance(self):
        """Fetch and display attendance dynamically."""
        attendance = view_student_attendance(self.student_id)

        if not attendance:
            messagebox.showinfo("Attendance", "No attendance records available.")
            return

        self.attendance_tree = self.create_table(["Date", "Class ID", "Status"])
        self.update_table(self.attendance_tree, attendance)

    def view_reviews(self):
        """Fetch and display student reviews dynamically."""
        conn = mysql.connector.connect(host="localhost", user="rootap", password="rootap123", database="schooldb")
        cursor = conn.cursor()

        query = """SELECT subject_id, review_text, date 
                   FROM review 
                   WHERE student_id = %s 
                   ORDER BY date DESC"""
        cursor.execute(query, (self.student_id,))
        reviews = cursor.fetchall()
        conn.close()

        if not reviews:
            messagebox.showinfo("Reviews", "No reviews available.")
            return

        reviews_tree = self.create_table(["Subject ID", "Review", "Date"])
        self.update_table(reviews_tree, reviews)

    def show_fee(self):
        """Fetch and display fee dynamically."""
        fee = view_student_fee(self.student_id)

        if not fee:
            messagebox.showinfo("fee", "No fee records available.")
            return

        self.fee_tree = self.create_table(["fee_id", "amount", "due_date", "paid"])
        self.update_table(self.fee_tree, fee)

    def update_table(self, tree, data):
        """Refresh table with new data."""
        for row in tree.get_children():
            tree.delete(row)  # Clear existing data
        for record in data:
            tree.insert("", "end", values=record)

if __name__ == "__main__":
    student_id = 2  # Replace with actual logged-in teacher's ID
    app = StudentDashboard(student_id)
    app.mainloop()