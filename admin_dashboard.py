# admin_dashboard.py
import tkinter as tk
import subprocess
import os
import csv
import sys
from tkinter import messagebox
from tkinter import ttk,filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import mysql.connector
# # Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
sys.path.append(os.path.dirname(current_dir))
from modules.student import add_student, fetch_students
from modules.teacher import add_teacher, fetch_teachers
from modules.classes import view_classes
from modules.attendance import mark_attendance

class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("800x500")
        self.resizable(False, False)
        self.configure(bg="#1ABC9C")  # Dark blue-gray background

        # Title Label
        tk.Label(self, text="Admin Dashboard", font=("Arial", 18, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

        # Frame for buttons
        button_frame = tk.Frame(self, bg="#1ABC9C")
        button_frame.pack(expand=True)

        # Button configurations (Icon path, Button Text, Command, Color, Width)
        buttons = [
            ("images/user.png", "Create User", self.open_create_user_window, "#F39C12", 12),
            ("images/viewUser.png", "View Users", self.open_view_user_window, "#E74C3C", 12),
            ("images/addStudent.png", "Add Student", self.add_student, "#3498DB", 12),
            ("images/viewStudents.png", "View Students", self.view_students, "#228B22", 12),
            ("images/teacher.png", "Add Teacher", self.add_teacher, "#F39C12", 12),
            ("images/viewTeachers.png", "View Teachers", self.view_teachers, "#E74C3C", 14),
            ("images/salary.png", "Teacher Salary", self.open_teacher_salary, "#3498DB", 14),
            ("images/classes.png", "View Classes", view_classes, "#228B22", 12),
            ("images/classFee.png", "Update Fees", self.open_update_fee, "#F39C12", 12),
            ("images/feeReceipt.png", "Generate Receipt", self.open_receipt_fee, "#E74C3C", 15),  # Wider Button
            ("images/markAttendance.png", "Mark Attendance", self.mark_student_attendance, "#3498DB", 15),  # Wider Button
            ("images/viewAttendance.png", "Attendance Report", self.open_attendance_report, "#228B22", 16),  # Wider Button
        ]

        # Arrange buttons in a grid
        for idx, (icon_path, text, command, color, width) in enumerate(buttons):
            row = idx // 4
            col = idx % 4
            self.create_icon_button(button_frame, icon_path, text, command, color, width).grid(row=row, column=col, padx=25, pady=15)  # Increased column spacing

        # Logout Button
        tk.Button(self, text="Logout", command=self.logout, bg="red", fg="white", font=("Arial", 12), width=15).pack(side="bottom", pady=10)

    def create_icon_button(self, parent, icon_path, text, command, color, width):
        """Creates an icon above a button"""
        frame = tk.Frame(parent, bg="#1ABC9C")

        # Load and resize icon
        try:
            img = Image.open(icon_path)
            img = img.resize((50, 50), Image.LANCZOS)
            icon = ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("Image Load Error", f"Error loading icon '{icon_path}': {e}")
            icon = None

        # Icon Label
        icon_label = tk.Label(frame, image=icon, bg="#1ABC9C")
        icon_label.image = icon  # Keep a reference
        icon_label.pack()

        # Button below the icon (Adjust width dynamically)
        btn = tk.Button(frame, text=text, command=command, bg=color, fg="white", font=("Arial", 10, "bold"), width=width)
        btn.pack(pady=5)

        return frame


    def logout(self):
        """Logout the admin and redirect to the login page."""
        self.destroy()
        subprocess.Popen(["python", "gui/login.py"])

    # Placeholder methods for button commands
    def open_create_user_window(self):
        pass

    def open_view_user_window(self):
        pass

    def add_student(self):
        pass

    def view_students(self):
        pass

    def add_teacher(self):
        pass

    def view_teachers(self):
        pass

    def open_teacher_salary(self):
        pass

    def view_classes(self):
        pass

    def open_update_fee(self):
        pass

    def open_receipt_fee(self):
        pass

    def mark_student_attendance(self):
        pass

    def open_attendance_report(self):
        pass
 

    def add_student(self):
        # New window for adding student details
        add_student_window = tk.Toplevel(self)
        add_student_window.title("Add Student")
        add_student_window.geometry("500x400")
        add_student_window.resizable(False, False)
        add_student_window.configure(bg="#1ABC9C")

        # Title Label
        title_label = tk.Label(
            add_student_window,
            text="Add Student",
            font=("Arial", 15, "bold"),
            bg="#1ABC9C",  # Teal color to match the View students theme
            fg="white",
            pady=10
        )
        title_label.pack(fill="x")


        # Frame for padding
        form_frame = tk.Frame(add_student_window, bg="#E3F2FD", padx=20, pady=10)
        form_frame.pack(pady=10,fill="both", expand=True)

        # Labels and Entry Fields
        tk.Label(form_frame, text="Full Name:", bg="#E3F2FD").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Grade:", bg="#E3F2FD").grid(row=1, column=0, sticky="w", pady=5)
        grade_var = tk.StringVar()
        grade_dropdown = ttk.Combobox(
            form_frame, textvariable=grade_var, 
            values=["1-3", "4-5", "6-10", "6-11", "11"],  # Adjusted to your options
            state="readonly", width=28
        )
        grade_dropdown.grid(row=1, column=1, pady=5)
        grade_dropdown.set("Select Grade")

        tk.Label(form_frame, text="Email:", bg="#E3F2FD").grid(row=2, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(form_frame, width=30)
        email_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Date of Birth:", bg="#E3F2FD").grid(row=3, column=0, sticky="w", pady=5)
        dob_entry = DateEntry(form_frame, width=27, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        dob_entry.grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="Address:", bg="#E3F2FD").grid(row=4, column=0, sticky="w", pady=5)
        address_entry = tk.Entry(form_frame, width=30)
        address_entry.grid(row=4, column=1, pady=5)

        tk.Label(form_frame, text="Phone Number:", bg="#E3F2FD").grid(row=5, column=0, sticky="w", pady=5)
        phone_no_entry = tk.Entry(form_frame, width=30)
        phone_no_entry.grid(row=5, column=1, pady=5)

        # ttk.Label(form_frame, text="User ID:").grid(row=6, column=0, sticky="w", pady=5)
        # user_id_entry = ttk.Entry(form_frame, width=30)
        # user_id_entry.grid(row=6, column=1, pady=5)

        def save_student():
            name = name_entry.get().strip()
            grade = grade_var.get()
            email = email_entry.get().strip()
            dob = dob_entry.get()
            address = address_entry.get().strip()
            phone_no = phone_no_entry.get().strip()

            if not name or grade == "Select Grade" or not email or not dob or not address or not phone_no:
                messagebox.showwarning("Missing Data", "Please fill all fields before saving!")
                return

            add_student(name, grade, email, dob, address, phone_no)
            messagebox.showinfo("Success", "Student added successfully!")
            add_student_window.destroy()

        # Save Button
        # ttk.Button(form_frame, text="Save Student", command=save_student, style="TButton").grid(row=6, column=0, columnspan=2, pady=15)

        button_frame = tk.Frame(add_student_window, bg="#1ABC9C")
        button_frame.pack(pady=10)

        save_button = tk.Button(
            button_frame, text="Save", command=save_student, font=("Arial", 12, "bold"),
            bg="#F39C12", fg="white", padx=20, pady=5, borderwidth=0, relief="ridge"
        )
        save_button.grid(row=0, column=0, padx=10)

        cancel_button = tk.Button(
            button_frame, text="Cancel", command=add_student_window.destroy, font=("Arial", 12, "bold"),
            bg="#D32F2F", fg="white", padx=20, pady=5, borderwidth=0, relief="ridge"
        )
        cancel_button.grid(row=0, column=1, padx=10)

        # Centering elements
        for i in range(7):
            form_frame.grid_columnconfigure(i, weight=1)

    def view_students(self):
        students = fetch_students()

        students_window = tk.Toplevel()
        students_window.title("View Students")
        students_window.geometry("800x400")
        students_window.configure(bg="#1ABC9C")

        # Title
        tk.Label(students_window, text="Student List", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

        # Search Bar
        search_frame = tk.Frame(students_window, bg="#1ABC9C")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search:", bg="#1ABC9C", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 12))
        search_entry.pack(side=tk.LEFT, padx=5)

        def search():
            query = search_entry.get().lower()
            for row in tree.get_children():
                values = tree.item(row)["values"]
                if any(str(val).lower().startswith(query) for val in values):
                    tree.selection_set(row)
                else:
                    tree.selection_remove(row)

        search_button = tk.Button(search_frame, text="Search", command=search, bg="#3498DB", fg="white", font=("Arial", 10))
        search_button.pack(side=tk.LEFT, padx=5)

        # Table (Treeview)
        columns = ("ID", "Name", "Grade", "Email", "DOB", "Address", "Phone number", "User ID")
        tree = ttk.Treeview(students_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=100, anchor="center")

        for row in students:
            tree.insert("", tk.END, values=row)

        tree.pack(pady=10, fill="both", expand=True)

        button_frame = tk.Frame(students_window, bg="#1ABC9C")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Edit Selected", command=lambda: edit_student(tree), bg="#F39C12", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Selected", command=lambda: delete_student(tree), bg="#E74C3C", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh", command=lambda: refresh_table(tree), bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Export to CSV", command=lambda: export_to_csv(tree), bg="#228B22", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=students_window.destroy, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

        def sort_column(tree, col, reverse):
            items = [(tree.set(k, col), k) for k in tree.get_children("")]
            items.sort(reverse=reverse)

            for index, (val, k) in enumerate(items):
                tree.move(k, "", index)

            tree.heading(col, text=col, command=lambda: sort_column(tree, col, not reverse))

        def refresh_table(tree):
            for row in tree.get_children():
                tree.delete(row)
            for row in fetch_students():
                tree.insert("", tk.END, values=row)
        
        # Function to export table data to CSV
        def export_to_csv(table):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Name", "Grade", "Email", "DOB", "Address", "Phone number", "User ID"])  # Header

                    for row_id in table.get_children():
                        writer.writerow(table.item(row_id)['values'])

                messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")

        
        # Function to edit student details
        def edit_student(table):
            selected_item = table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a student to edit.")
                return

            # Get selected student details
            student_details = table.item(selected_item)["values"]

            # Create Edit Window
            edit_window = tk.Toplevel()
            edit_window.title("Edit Student Details")
            edit_window.geometry("500x520")
            edit_window.resizable(False, False)
            edit_window.configure(bg="#1ABC9C")

            # Title Label
            title_label = tk.Label(
                    edit_window,
                    text="Edit Student Details",
                    font=("Arial", 15, "bold"),
                    bg="#1ABC9C",  # Teal color to match the View students theme
                    fg="white",
                    pady=10
                )
            title_label.pack(fill="x")

            # Frame for padding
            form_frame = tk.Frame(edit_window, bg="#E3F2FD", padx=20, pady=10)
            form_frame.pack(pady=10,fill="both", expand=True)

            # Labels and Entry Fields
            labels = ["ID", "Name", "Grade", "Email","DOB","Address","Phone number","User ID"]
            entries = {}

            for i, label in enumerate(labels):
                tk.Label(form_frame, text=label,bg="#E3F2FD").pack(pady=2)
                entry = tk.Entry(form_frame)
                entry.pack(pady=2)
                entry.insert(0, student_details[i])
                if label == "ID":
                    entry.config(state="readonly")  # ID should not be editable
                entries[label] = entry

            # Save Button
            def save_changes():
                student_id = entries["ID"].get()
                sName = entries["Name"].get()
                grade = entries["Grade"].get()
                email = entries["Email"].get()
                dob = entries["DOB"].get()
                address = entries["Address"].get()
                phoneNo = entries["Phone number"].get()
                userId = entries["User ID"].get()

                def connect():

                    return mysql.connector.connect(
                    host = "localhost",
                    user = "rootap",
                    password = "rootap123",
                    database = "schooldb"
                )
                conn = connect()
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE student 
                    SET name=%s, grade=%s,  email=%s, dob=%s, address=%s, phone_no=%s, user_id=%s
                    WHERE student_id=%s
                """, ( sName, grade, email, dob,address,phoneNo,userId, student_id ))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Student details updated successfully!")
                edit_window.destroy()
                # refresh_table(table, fetch_students())

            tk.Button(edit_window, text="Save", command=save_changes, bg="green", fg="white").pack(pady=10)

        def delete_student(table):
            selected_item = table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a student to delete.")
                return

            student_id = table.item(selected_item)["values"][0]  # Get Student ID

            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete student ID {student_id}?")
            if not confirm:
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="rootap",
                    password="rootap123",
                    database="schooldb"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Student deleted successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {e}")


    def add_teacher(self):
        add_teacher_window = tk.Toplevel()
        add_teacher_window.title("Add Teacher")
        add_teacher_window.geometry("500x400")
        add_teacher_window.resizable(False, False)
        add_teacher_window.configure(bg="#1ABC9C")  # Light blue background

        # Title Label
        title_label = tk.Label(
            add_teacher_window,
            text="Add Teacher",
            font=("Arial", 15, "bold"),
            bg="#1ABC9C",  # Teal color to match the View Teachers theme
            fg="white",
            pady=10
        )
        title_label.pack(fill="x")

        form_frame = tk.Frame(add_teacher_window, bg="#E3F2FD", padx=20, pady=10)
        form_frame.pack(pady=10, fill="both", expand=True)

        # # Labels and Entry Fields
        # labels = ["Name:", "Email:", "Subject ID:", "User ID:"]
        # entries = {}
        
        # for i, text in enumerate(labels):
        #     tk.Label(form_frame, text=text, bg="#E3F2FD").grid(row=i, column=0, sticky="w", pady=5)
        #     entry = ttk.Entry(form_frame, width=30)
        #     entry.grid(row=i, column=1, pady=5, padx=10)
        #     entries[text] = entry

        # Labels and Entry Fields
        tk.Label(form_frame, text="Name:", bg="#E3F2FD").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Email:", bg="#E3F2FD").grid(row=1, column=0, sticky="w", pady=5)
        email_entry = tk.Entry(form_frame, width=30)
        email_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Phone Number:", bg="#E3F2FD").grid(row=2, column=0, sticky="w", pady=5)
        phone_no_entry = tk.Entry(form_frame, width=30)
        phone_no_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Subject ID:", bg="#E3F2FD").grid(row=3, column=0, sticky="w", pady=5)
        subject_entry = tk.Entry(form_frame, width=30)
        subject_entry.grid(row=3, column=1, pady=5)

        # tk.Label(form_frame, text="Date of Birth:", bg="#E3F2FD").grid(row=3, column=0, sticky="w", pady=5)
        # dob_entry = DateEntry(form_frame, width=27, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        # dob_entry.grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="User ID:", bg="#E3F2FD").grid(row=4, column=0, sticky="w", pady=5)
        user_entry = tk.Entry(form_frame, width=30)
        user_entry.grid(row=4, column=1, pady=5)

        

        # ttk.Label(form_frame, text="User ID:").grid(row=6, column=0, sticky="w", pady=5)
        # user_id_entry = ttk.Entry(form_frame, width=30)
        # user_id_entry.grid(row=6, column=1, pady=5)

        # Save Button
        def save_teacher():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phoneNo = phone_no_entry.get().strip()
            subject = subject_entry.get().strip()
            user = user_entry.get().strip()

            if not name or not email or not phoneNo or not subject or not user:
                messagebox.showwarning("Missing Data", "Please fill all fields before saving!")
                return
            
            # Call the function to add teacher (Assumed to exist)
            add_teacher(name, email,phoneNo, subject, user)
            
            
            add_teacher_window.destroy()

        button_frame = tk.Frame(add_teacher_window, bg="#1ABC9C")
        button_frame.pack(pady=10)

        save_button = tk.Button(
            button_frame, text="Save", command=save_teacher, font=("Arial", 12, "bold"),
            bg="#F39C12", fg="white", padx=20, pady=5, borderwidth=0, relief="ridge"
        )
        save_button.grid(row=0, column=0, padx=10)

        cancel_button = tk.Button(
            button_frame, text="Cancel", command=add_teacher_window.destroy, font=("Arial", 12, "bold"),
            bg="#D32F2F", fg="white", padx=20, pady=5, borderwidth=0, relief="ridge"
        )
        cancel_button.grid(row=0, column=1, padx=10)
    

    def view_teachers(self):
        teachers = fetch_teachers()

        # """Create a window to display Teacher data in a table format."""
        teachers_window = tk.Toplevel()
        teachers_window.title("View Teachers")
        teachers_window.geometry("750x400")
        teachers_window.configure(bg="#1ABC9C")

        # Title
        tk.Label(teachers_window, text="Teacher List", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

        # Search Bar
        search_frame = tk.Frame(teachers_window, bg="#1ABC9C")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search:", bg="#1ABC9C", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 12))
        search_entry.pack(side=tk.LEFT, padx=5)
        
        def search():
            # """Filter the table based on search input."""
            query = search_entry.get().lower()
            for row in tree.get_children():
                values = tree.item(row)["values"]
                if any(str(val).lower().startswith(query) for val in values):
                    tree.selection_set(row)  # Highlight matching row
                else:
                    tree.selection_remove(row)

        search_button = tk.Button(search_frame, text="Search", command=search, bg="#3498DB", fg="white", font=("Arial", 10))
        search_button.pack(side=tk.LEFT, padx=5)

        # Table (Treeview)
        columns = ("ID", "Name", "Email","Phone No","Subject ID","User ID")
        tree = ttk.Treeview(teachers_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))  # Sortable columns
            tree.column(col, width=100, anchor="center")

        # Insert data into table
        for row in teachers:
            tree.insert("", tk.END, values=row)

        tree.pack(pady=10, fill="both", expand=True)

        button_frame = tk.Frame(teachers_window, bg="#1ABC9C")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Edit Selected", command=lambda: edit_teacher(tree), bg="#F39C12", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Selected", command=lambda: delete_teacher(tree), bg="#E74C3C", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Export to CSV", command=lambda: export_to_csv(tree), bg="#228B22", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh", command=lambda: refresh_table(tree), bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=teachers_window.destroy, bg="red", fg="white").pack(side=tk.LEFT, padx=5)


        def sort_column(tree, col, reverse):
            # """Sort the Treeview column."""
            items = [(tree.set(k, col), k) for k in tree.get_children("")]
            items.sort(reverse=reverse)

            for index, (val, k) in enumerate(items):
                tree.move(k, "", index)

            tree.heading(col, text=col, command=lambda: sort_column(tree, col, not reverse))  # Toggle sort order


        def refresh_table(tree):
        #     """Refresh the Treeview with updated data."""
            for row in tree.get_children():
                tree.delete(row)  # Clear the table

            for row in fetch_teachers():
                tree.insert("", tk.END, values=row)  # Reinsert updated data

        # Function to export table data to CSV
        def export_to_csv(table):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Name", "Email","Subject ID","User ID"])  # Header

                    for row_id in table.get_children():
                        writer.writerow(table.item(row_id)['values'])

                messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")
        
        # Function to edit teacher details
        def edit_teacher(table):
            selected_item = table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a teacher to edit.")
                return

            # Get selected teacher details
            teacher_details = table.item(selected_item)["values"]

            # Create Edit Window
            edit_window = tk.Toplevel()
            edit_window.title("Edit Teacher Details")
            edit_window.geometry("400x420")
            edit_window.resizable(False, False)
            edit_window.configure(bg="#1ABC9C")

            # Title Label
            title_label = tk.Label(
                    edit_window,
                    text="Edit Teacher Details",
                    font=("Arial", 15, "bold"),
                    bg="#1ABC9C",  # Teal color to match the View students theme
                    fg="white",
                    pady=10
                )
            title_label.pack(fill="x")

            # Frame for padding
            form_frame = tk.Frame(edit_window, bg="#E3F2FD", padx=20, pady=10)
            form_frame.pack(pady=10,fill="both", expand=True)

            # Labels and Entry Fields
            labels = ["ID", "Name", "Email","Phone No","Subject ID","User ID"]
            entries = {}

            for i, label in enumerate(labels):
                tk.Label(form_frame, text=label,bg="#E3F2FD").pack(pady=2)
                entry = tk.Entry(form_frame)
                entry.pack(pady=2)
                entry.insert(0, teacher_details[i])
                if label == "ID":
                    entry.config(state="readonly")  # ID should not be editable
                entries[label] = entry

            # Save Button
            def save_changes():
                teacher_id = entries["ID"].get()
                tName = entries["Name"].get()
                email = entries["Email"].get()
                phone = entries["Phone No"].get()
                subject = entries["Subject ID"].get()
                user = entries["User ID"].get()
                # phoneNo = entries["Phone number"].get()

                def connect():

                    return mysql.connector.connect(
                    host = "localhost",
                    user = "rootap",
                    password = "rootap123",
                    database = "schooldb"
                )
                conn = connect()
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE teacher 
                    SET name=%s, email=%s,phone_no=%s, subject_id=%s, user_id=%s
                    WHERE teacher_id=%s
                """, ( tName,  email,phone, subject,user,teacher_id ))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Teacher details updated successfully!")
                edit_window.destroy()
                # refresh_table(table, fetch_teacher())

            tk.Button(edit_window, text="Save", command=save_changes, bg="green", fg="white").pack(pady=10)   

        def delete_teacher(table):
            selected_item = table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a teacher to delete.")
                return

            teacher_id = table.item(selected_item)["values"][0]  # Get Teacher ID

            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete teacher ID {teacher_id}?")
            if not confirm:
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="rootap",
                    password="rootap123",
                    database="schooldb"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM teacher WHERE teacher_id = %s", (teacher_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Teacher deleted successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete teacher: {e}")    

    def open_teacher_salary(self):
        """Open the Teacher Salary window by running teacherSalary.py."""
        script_path = os.path.abspath(r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\modules\teacherSalary.py")
        subprocess.Popen(["python", script_path])   


    def mark_student_attendance(self):
        # New window for marking attendance
        attendance_window = tk.Toplevel(self)
        attendance_window.title("Mark Attendance")
        attendance_window.geometry("500x400")
        attendance_window.resizable(False, False)
        attendance_window.configure(bg="#1ABC9C")

        # Title Label
        title_label = tk.Label(
            attendance_window,
            text="Mark Attendance",
            font=("Arial", 15, "bold"),
            bg="#1ABC9C",  # Teal color to match the View students theme
            fg="white",
            pady=10
        )
        title_label.pack(fill="x")

        # Frame for padding
        form_frame = tk.Frame(attendance_window, bg="#E3F2FD", padx=20, pady=10)
        form_frame.pack(pady=10,fill="both", expand=True)

        tk.Label(form_frame, text="Student ID", bg="#E3F2FD").grid(row=0, column=0, sticky="w", pady=5)
        student_id_entry = tk.Entry(form_frame, width=30)
        student_id_entry.grid(row=0, column=1, pady=5)

        # tk.Label(form_frame, text="Full Name:", bg="#E3F2FD").grid(row=0, column=0, sticky="w", pady=5)
        # name_entry = tk.Entry(form_frame, width=30)
        # name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Date ", bg="#E3F2FD").grid(row=1, column=0, sticky="w", pady=5)
        date_entry =  DateEntry(form_frame, width=27, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        date_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Class ID", bg="#E3F2FD").grid(row=2, column=0, sticky="w", pady=5)
        class_entry = tk.Entry(form_frame, width=30)
        class_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Status", bg="#E3F2FD").grid(row=3, column=0, sticky="w", pady=5)
        status_var = tk.StringVar()
        status_dropdown = ttk.Combobox(
            form_frame, textvariable=status_var, 
            values=["Present", "Absent"],
            state="readonly", width=28
        )
        status_dropdown.grid(row=3, column=1, pady=5)
        status_dropdown.set("Present")


        def save_attendance():
            student_id = student_id_entry.get()
            date = date_entry.get()
            classId = class_entry.get()
            status = status_var.get()

            if not student_id or status == "Select Present" or not date or not classId :
                messagebox.showwarning("Missing Data", "Please fill all fields before saving!")
                return
            
            mark_attendance(student_id, classId, status, date)
            messagebox.showinfo("Success", "Attendance marked successfully")
            attendance_window.destroy()

        # tk.Button(attendance_window, text="Save", command=save_attendance).grid(row=4, column=1)

        button_frame = tk.Frame(attendance_window, bg="#1ABC9C")
        button_frame.pack(pady=10)

        save_button = tk.Button(
            button_frame, text="Save", command=save_attendance, font=("Arial", 12, "bold"),
            bg="#F39C12", fg="white", padx=20, pady=5, borderwidth=0, relief="ridge"
        )
        save_button.grid(row=0, column=0, padx=10)

        cancel_button = tk.Button(
            button_frame, text="Cancel", command=attendance_window.destroy, font=("Arial", 12, "bold"),
            bg="#D32F2F", fg="white", padx=20, pady=5, borderwidth=0, relief="ridge"
        )
        cancel_button.grid(row=0, column=1, padx=10)

        # Centering elements
        for i in range(7):
            form_frame.grid_columnconfigure(i, weight=1)
    
    def open_create_user_window(self):
        """Open the create user window by running createUser.py."""
        script_path = os.path.abspath(r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\modules\createUser.py")
        subprocess.Popen(["python", script_path])
    
    def open_view_user_window(self):
        """Open the view user window by running viewUser.py."""
        script_path = os.path.abspath(r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\modules\viewUser.py")
        subprocess.Popen(["python", script_path])

    
    def open_attendance_report(self):
        """Open the Attendance Report window by running attendanceReport.py."""
        script_path = os.path.abspath(r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\gui\attendanceReport.py")
        subprocess.Popen(["python", script_path])

    def open_update_fee(self):
        """Open the Class Fee window by running updateFee.py."""
        script_path = os.path.abspath(r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\modules\updateFee.py")
        subprocess.Popen(["python", script_path])

    def open_receipt_fee(self):
        """Open the Receipt Fee Generator window by running receiptForFees.py."""
        script_path = os.path.abspath(r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\gui\receiptForFees.py")
        subprocess.Popen(["python", script_path])
    
        


if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
