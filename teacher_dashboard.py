# teacher_dashboard.py
import tkinter as tk
import subprocess
import os
import sys
import csv
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
# # Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
sys.path.append(os.path.dirname(current_dir))
from modules.grading import get_student_marks_by_teacher,add_student_marks, update_student_marks
import mysql.connector
def connect():
            return mysql.connector.connect(
                host="localhost",
                user="rootap",
                password="rootap123",
                database="schooldb"
            )
class TeacherDashboard(tk.Tk):
    def __init__(self, user_id,teacher_id=None):
        super().__init__()
        self.user_id = user_id
        self.teacher_id = teacher_id if teacher_id is not None else self.get_teacher_id()  # Retrieve teacher_id from user_id

        self.title("Teacher Dashboard")
        self.geometry("800x500")
        self.resizable(False, False)
        self.configure(bg="#1ABC9C") 

        # Title
        tk.Label(self, text="Teacher Dashboard", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

        if not self.teacher_id:
            tk.Label(self, text="Error: Teacher ID not found", fg="white", bg="#1ABC9C", font=("Arial", 12)).pack()

        # Logout Function
        def logout():
            """Logout the teacher and redirect to the login page."""
            self.destroy()
            subprocess.Popen(["python", "gui/login.py"])

        self.table_frame = tk.Frame(self, bg="#2C3E50")
        self.table_frame.pack(pady=20)

        self.marks_tree = None  # Placeholder for marks table



        # Frame for Icons and Buttons
        btn_frame = tk.Frame(self, bg="#1ABC9C")
        btn_frame.pack(expand=True)

        # Button Details (icon path, text, command)
        buttons = [
            ("images/viewStudents.png", "View Students", self.view_students),
            ("images/addMarks.png", "Add Marks", self.add_marks_window),
            ("images/viewMarks.png", "View & Update Marks", self.view_update_marks),
            ("images/reviewStudent.png", "Give Student Reviews", self.open_student_review),
            ("images/viewReviews.png", "Generate Review Report", self.open_review_report)
        ]

        # Load and display buttons with icons in a grid (2 columns)
        for i, (icon_path, text, command) in enumerate(buttons):
            img = Image.open(icon_path).resize((50, 50), Image.LANCZOS)  # Resize icon
            img = ImageTk.PhotoImage(img)

            col = i % 2  # Two columns
            row = i // 2  # New row every 2 items

            # Icon
            label = tk.Label(btn_frame, image=img, bg="#1ABC9C")
            label.image = img  # Keep reference
            label.grid(row=row * 2, column=col, padx=20, pady=10)  # Place the icon on a separate row

            # Button (Updated color to `#F39C12`)
            btn = tk.Button(
                btn_frame, text=text, command=command, 
                bg="#F39C12", fg="white", font=("Arial", 10, "bold"), width=20
            )
            btn.grid(row=(row * 2) + 1, column=col, padx=20, pady=5)  # Button placed below the icon

        # Logout Button
        logout_button = tk.Button(self, text="Logout", command=logout, bg="red", fg="white", font=("Arial", 12))
        logout_button.pack(side="bottom", pady=10)


        # # Logout Button
        # logout_button = tk.Button(self, text="Logout", command=logout, bg="red", fg="white", font=("Arial", 12))
        # logout_button.pack(side="bottom", pady=10)

        
    # Placeholder methods
    def view_students(self):
        pass

    def open_student_review(self):
        pass

    def open_review_report(self):
        pass

    def view_update_marks(self):
        pass

    def add_marks_window(self):
        pass

    def get_teacher_id(self):
        return 1  # Replace with real logic

    def get_teacher_id(self):
        # """Fetch the teacher_id linked to this user_id."""
        conn=connect()
        cursor = conn.cursor()
        cursor.execute("SELECT teacher_id FROM teacher WHERE user_id = %s", (self.user_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None  # Return teacher_id if found, otherwise None

        
    
    def fetch_students(self):
    # """Fetch students taught by this teacher."""
        if not self.teacher_id:
            return []

        conn = connect()
        cursor = conn.cursor()

        query = """
        SELECT s.student_id, s.name, s.grade, s.email, s.dob, s.address, s.phone_no
        FROM student s
        JOIN studentclass sc ON s.student_id = sc.student_id
        JOIN class c ON sc.class_id = c.class_id
        WHERE c.teacher_id = %s
        """
        
        cursor.execute(query, (self.teacher_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    
    def view_students(self):
        # """Show students of the teacher in a new window."""
        students_window = tk.Toplevel(self)
        students_window.title("View Students")
        students_window.geometry("800x500")
        students_window.configure(bg="#1ABC9C")

        tk.Label(students_window, text="My Students", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

        # Search Bar
        search_frame = tk.Frame(students_window, bg="#1ABC9C")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search:", bg="#1ABC9C", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 12))
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Table (Treeview)
        columns = ("ID", "Name", "Grade", "Email", "DOB", "Address", "Phone No")
        tree = ttk.Treeview(students_window, columns=columns, show="headings")

        def sort_column(tree, col, reverse):
            """Sort the Treeview column."""
            items = [(tree.set(k, col), k) for k in tree.get_children("")]
            items.sort(reverse=reverse)

            for index, (val, k) in enumerate(items):
                tree.move(k, "", index)

            tree.heading(col, text=col, command=lambda: sort_column(tree, col, not reverse))  # Toggle sort order

        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))  # Sortable columns
            tree.column(col, width=100, anchor="center")

        tree.pack(pady=10, fill="both", expand=True)

        # Insert initial data
        self.refresh_table(tree)

        # Search Function
        def search():
            query = search_entry.get().lower()
            for row in tree.get_children():
                values = tree.item(row)["values"]
                if any(str(val).lower().startswith(query) for val in values):
                    tree.selection_set(row)  # Highlight matching row
                else:
                    tree.selection_remove(row)

        search_button = tk.Button(search_frame, text="Search", command=search, bg="#3498DB", fg="white", font=("Arial", 10))
        search_button.pack(side=tk.LEFT, padx=5)

        button_frame = tk.Frame(students_window, bg="#1ABC9C")
        button_frame.pack(pady=10)
        # Refresh Button
        tk.Button(button_frame, text="Refresh", command=lambda: self.refresh_table(tree), bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Close", command=students_window.destroy, bg="red", fg="white").pack(side=tk.LEFT, padx=10)

    def refresh_table(self, tree):
        # """Refresh the table with updated student data."""
        for row in tree.get_children():
            tree.delete(row)  # Clear table

        for row in self.fetch_students():
            tree.insert("", tk.END, values=row)  # Reinsert updated data
    
    def add_marks_window(self):
        """Open a window for adding student marks."""
        add_window = tk.Toplevel(self)
        add_window.title("Add Student Marks")
        add_window.geometry("500x400")
        add_window.resizable(False, False)
        add_window.configure(bg="#1ABC9C")

        # Title Label
        title_label = tk.Label(
                add_window,
                text="Add Student Marks",
                font=("Arial", 15, "bold"),
                bg="#1ABC9C",  # Teal color to match the View students theme
                fg="white",
                pady=10
            )
        title_label.pack(fill="x")

        # Frame for padding
        form_frame = tk.Frame(add_window, bg="#E3F2FD", padx=20, pady=10)
        form_frame.pack(pady=10,fill="both", expand=True)

        tk.Label(form_frame, text="Test ID:", bg="#E3F2FD").pack(pady=5)
        test_id_entry = tk.Entry(form_frame, width=30)
        test_id_entry.pack()

        tk.Label(form_frame, text="Subject ID:", bg="#E3F2FD").pack(pady=5)
        subject_id_entry = tk.Entry(form_frame, width=30)
        subject_id_entry.pack()

        tk.Label(form_frame, text="Student ID:", bg="#E3F2FD").pack(pady=5)
        student_id_entry = tk.Entry(form_frame, width=30)
        student_id_entry.pack()

        tk.Label(form_frame, text="Marks:", bg="#E3F2FD").pack(pady=5)
        marks_entry = tk.Entry(form_frame, width=30)
        marks_entry.pack()

        def submit_marks():
            test_id = test_id_entry.get()
            subject_id = subject_id_entry.get()
            student_id = student_id_entry.get()
            marks = marks_entry.get()

            if not (test_id and subject_id and student_id  and marks):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                marks = float(marks)
                add_student_marks(test_id, subject_id, student_id, marks)
                messagebox.showinfo("Success", "Marks added successfully!")
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input for marks!")

        button_frame = tk.Frame(add_window, bg="#1ABC9C")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Submit", command=submit_marks,bg="#E3F2FD").pack(pady=10)


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

    def view_update_marks(self):
        """Open a separate window to view and update student marks."""
        marks_window = tk.Toplevel(self)
        marks_window.title("View & Update Marks")
        marks_window.geometry("750x400")
        marks_window.configure(bg="#1ABC9C")


        tk.Label(marks_window, text="Student Marks", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

        marks = get_student_marks_by_teacher(self.teacher_id)
        if not marks:
            messagebox.showinfo("Marks", "No marks available.")
            marks_window.destroy()
            return

        columns = ["Test ID", "Student ID", "Subject ID", "Marks"]
        tree = ttk.Treeview(marks_window, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(pady=10, fill="both", expand=True)

        for record in marks:
            tree.insert("", "end", values=record)

        self.marks_tree = tree

        # def edit_marks():
        #     """Open an editing window for updating student marks."""
        #     selected_item = tree.selection()
        #     if not selected_item:
        #         messagebox.showwarning("Warning", "Please select a record to edit.")
        #         return

        #     item_values = tree.item(selected_item, "values")
        #     test_id, student_id, subject_id, marks = item_values

        #     edit_window = tk.Toplevel(marks_window)
        #     edit_window.title("Edit Marks")
        #     edit_window.geometry("400x400")
        #     edit_window.resizable(False, False)
        #     edit_window.configure(bg="#1ABC9C")

        #     # Title Label
        #     title_label = tk.Label(
        #             edit_window,
        #             text="Edit Marks",
        #             font=("Arial", 15, "bold"),
        #             bg="#1ABC9C",  # Teal color to match the View students theme
        #             fg="white",
        #             pady=10
        #         )
        #     title_label.pack(fill="x")

        #     # Frame for padding
        #     form_frame = tk.Frame(edit_window, bg="#E3F2FD", padx=20, pady=10)
        #     form_frame.pack(pady=10,fill="both", expand=True)


        #     # tk.Label(form_frame , text="Edit Marks", font=("Arial", 14, "bold"), bg="#34495E", fg="white").pack(pady=10)

        #     tk.Label(form_frame , text="Marks:", bg="#E3F2FD").pack()
        #     marks_entry = tk.Entry(form_frame, width=20)
        #     marks_entry.insert(0, marks)
        #     marks_entry.pack()

        #     def save_changes():
        #         new_marks = marks_entry.get()
        #         if not new_marks.isdigit():
        #             messagebox.showerror("Error", "Marks must be a number.")
        #             return

        #         update_student_marks(test_id, student_id, subject_id, int(new_marks))
        #         messagebox.showinfo("Success", "Marks updated successfully.")
        #         edit_window.destroy()
        #         marks_window.destroy()
        #         self.view_update_marks()  # Reopen updated marks window

        #     tk.Button(edit_window, text="Save Changes", command=save_changes, bg="#E3F2FD").pack(pady=10)

        
        def edit_marks():
            # """Open an editing window for updating student marks."""
            selected_item = self.marks_tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a record to edit.")
                return

            item_values = self.marks_tree.item(selected_item, "values")
            test_id, student_id, subject_id, marks = item_values

            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Marks")
            edit_window.geometry("400x400")
            edit_window.configure(bg="#1ABC9C")
            edit_window.resizable(False,False)

                # Title Label
            title_label = tk.Label(
                edit_window,
                text="Edit Marks",
                font=("Arial", 15, "bold"),
                bg="#1ABC9C",  # Teal color to match the View students theme
                fg="white",
                pady=10
            )
            title_label.pack(fill="x")


            # Frame for padding
            form_frame = tk.Frame(edit_window, bg="#E3F2FD", padx=20, pady=10)
            form_frame.pack(pady=10,fill="both", expand=True)

            # tk.Label(form_frame, text="Edit Marks", font=("Arial", 14, "bold"), bg="#E3F2FD", fg="white").pack(pady=10)

            tk.Label(form_frame, text="Test ID:", bg="#E3F2FD").pack()
            test_id_entry = tk.Entry(form_frame, width=20)
            test_id_entry.insert(0, test_id)
            test_id_entry.pack()

            tk.Label(form_frame, text="Student ID:",bg="#E3F2FD").pack()
            student_id_entry = tk.Entry(form_frame, width=20)
            student_id_entry.insert(0, student_id)
            student_id_entry.pack()

            tk.Label(form_frame, text="Subject ID:", bg="#E3F2FD").pack()
            subject_id_entry = tk.Entry(form_frame, width=20)
            subject_id_entry.insert(0, subject_id)
            subject_id_entry.pack()

            tk.Label(form_frame, text="Marks:", bg="#E3F2FD").pack()
            marks_entry = tk.Entry(form_frame, width=20)
            marks_entry.insert(0, marks)
            marks_entry.pack()

            def save_changes():
                new_test_id = test_id_entry.get().strip()
                new_student_id = student_id_entry.get().strip()  # Keep as string (VARCHAR)
                new_subject_id = subject_id_entry.get().strip()  # Keep as string (VARCHAR)
                new_marks = marks_entry.get().strip()

                # Validate Inputs
                if not new_test_id.isdigit() or not new_marks.isdigit():
                    messagebox.showerror("Error", "Test ID and Marks must be numbers.")
                    return

                # Call Update Function
                update_student_marks(
                    old_test_id=test_id, old_student_id=student_id, old_subject_id=subject_id,
                    new_test_id=int(new_test_id), new_student_id=new_student_id,
                    new_subject_id=new_subject_id, new_marks=int(new_marks)
                )

                messagebox.showinfo("Success", "Marks updated successfully.")
                edit_window.destroy()

                # Refresh Table
                for row in self.marks_tree.get_children():
                    self.marks_tree.delete(row)

                new_marks_data = get_student_marks_by_teacher(self.teacher_id)
                for record in new_marks_data:
                    self.marks_tree.insert("", "end", values=record)
            
            button_frame = tk.Frame(edit_window, bg="#1ABC9C")
            button_frame.pack(pady=10)
            tk.Button(button_frame, text="Save Changes", command=save_changes, bg="#E3F2FD").pack(pady=10)

            # def update_student_marks(test_id, student_id, subject_id, new_marks):
            #     conn = connect()
            #     cursor = conn.cursor()
            #     print(f"Updating marks: Test ID={test_id}, Student ID={student_id}, Subject ID={subject_id}, New Marks={new_marks}")  # Debugging
            #     query = "UPDATE studentmark SET marks = %s WHERE test_id = %s AND student_id = %s AND subject_id = %s"
            #     cursor.execute(query, (new_marks, test_id, student_id, subject_id))
            #     conn.commit()  # Ensure changes are saved

            def update_student_marks(old_test_id, old_student_id, old_subject_id, new_test_id, new_student_id, new_subject_id, new_marks):
                conn = connect()
                cursor = conn.cursor()
                print(f"Updating: Test={old_test_id} → {new_test_id}, Student={old_student_id} → {new_student_id}, Subject={old_subject_id} → {new_subject_id}, Marks={new_marks}")

                query = """
                    UPDATE studentmark 
                    SET test_id = %s, student_id = %s, subject_id = %s, marks = %s 
                    WHERE test_id = %s AND student_id = %s AND subject_id = %s
                """
                cursor.execute(query, (new_test_id, new_student_id, new_subject_id, new_marks, old_test_id, old_student_id, old_subject_id))
                conn.commit()
        
        button_frame = tk.Frame(marks_window, bg="#1ABC9C")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Edit Marks", command=edit_marks, bg="#F39C12", fg="white", width=15).pack( padx=5)
            

        #     def save_changes():
        #         new_marks = marks_entry.get()
        #         if not new_marks.isdigit():
        #             messagebox.showerror("Error", "Marks must be a number.")
        #             return

        #         update_student_marks(test_id, student_id, subject_id, int(new_marks))
        #         messagebox.showinfo("Success", "Marks updated successfully.")

        #         edit_window.destroy()
                
        #         # ✅ Clear existing data and reload updated marks
        #         for row in self.marks_tree.get_children():
        #             self.marks_tree.delete(row)
                
        #         new_marks_data = get_student_marks_by_teacher(self.teacher_id)
        #         for record in new_marks_data:
        #             self.marks_tree.insert("", "end", values=record)
        #         # self.view_update_marks()  # Refresh table

        #     tk.Button(edit_window, text="Save Changes", command=save_changes, bg="#27AE60", fg="white").pack(pady=10)
        # tk.Button(marks_window, text="Edit Marks", command=edit_marks, bg="#E67E22", fg="white", width=15).pack(side=tk.LEFT, padx=5)

        # -------------------------
        
        # def edit_marks():
        #     """Open an editing window for updating student marks."""
        #     selected_item = tree.selection()
        #     if not selected_item:
        #         messagebox.showwarning("Warning", "Please select a record to edit.")
        #         return

        #     item_values = tree.item(selected_item, "values")
        #     test_id, student_id, subject_id, marks = item_values

        #     edit_window = tk.Toplevel(marks_window)
        #     edit_window.title("Edit Marks")
        #     edit_window.geometry("300x250")
        #     edit_window.configure(bg="#34495E")

        #     tk.Label(edit_window, text="Edit Marks", font=("Arial", 14, "bold"), bg="#34495E", fg="white").pack(pady=10)
        #     tk.Label(edit_window, text="Marks:", bg="#34495E", fg="white").pack()
        #     marks_entry = tk.Entry(edit_window, width=20)
        #     marks_entry.insert(0, marks)
        #     marks_entry.pack()

        #     def save_changes():
        #         new_marks = marks_entry.get()
        #         if not new_marks.isdigit():
        #             messagebox.showerror("Error", "Marks must be a number.")
        #             return

        #         update_student_marks(test_id, student_id, subject_id, int(new_marks))
        #         messagebox.showinfo("Success", "Marks updated successfully.")
        #         edit_window.destroy()
        #         marks_window.destroy()
        #         self.view_update_marks()  # Reopen updated marks window

        #     tk.Button(edit_window, text="Save Changes", command=save_changes, bg="#27AE60", fg="white").pack(pady=10)

        # button_frame = tk.Frame(marks_window, bg="#1ABC9C")
        # button_frame.pack(pady=10)

        # tk.Button(button_frame, text="Edit Marks", command=edit_marks, bg="#E67E22", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        # # tk.Button(button_frame, text="Delete Selected", command=lambda: delete_marks(tree), bg="#E74C3C", fg="white").pack(side=tk.LEFT, padx=5)
        # tk.Button(button_frame, text="Refresh", command=lambda: refresh_table(tree), bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=5)
        # tk.Button(button_frame, text="Export to CSV", command=lambda: export_to_csv(tree), bg="#228B22", fg="white").pack(side=tk.LEFT, padx=5)
        # tk.Button(button_frame, text="Close", command=marks_window.destroy, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

        def sort_column(tree, col, reverse):
            items = [(tree.set(k, col), k) for k in tree.get_children("")]
            items.sort(reverse=reverse)

            for index, (val, k) in enumerate(items):
                tree.move(k, "", index)

            tree.heading(col, text=col, command=lambda: sort_column(tree, col, not reverse))
        
        def refresh_table(tree):
            for row in tree.get_children():
                tree.delete(row)
            for row in get_student_marks_by_teacher(self.teacher_id):
                tree.insert("", tk.END, values=row)
        
        # Function to export table data to CSV
        def export_to_csv(table):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Test ID", "Student ID", "Subject ID", "Marks"])  # Header

                    for row_id in table.get_children():
                        writer.writerow(table.item(row_id)['values'])

                messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")

    def open_review_report(self):
        # """Open the Review Report window by running reviewReport.py."""
        script_path = os.path.abspath(r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\gui\reviewsReport.py")
        subprocess.Popen(["python", script_path])  


    # def view_update_marks(self):
    #     # """Fetch and display student marks dynamically."""
    #     marks = get_student_marks_by_teacher(self.teacher_id)

    #     if not marks:
    #         messagebox.showinfo("Marks", "No marks available.")
    #         return

    #     self.marks_tree = self.create_table(["Test ID", "Student ID", "Subject ID", "Marks"])

    #     for row in self.marks_tree.get_children():
    #         self.marks_tree.delete(row)  # Clear existing data

    #     for record in marks:
    #         self.marks_tree.insert("", "end", values=record)

    #     # Add an "Edit Marks" button
    #     tk.Button(self.table_frame, text="Edit Marks", command=self.edit_marks, bg="#E67E22", fg="white", width=15).pack(pady=10)

    def edit_marks(self):
        # """Open an editing window for updating student marks."""
        selected_item = self.marks_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to edit.")
            return

        item_values = self.marks_tree.item(selected_item, "values")
        test_id, student_id, subject_id, marks = item_values

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Marks")
        edit_window.geometry("300x250")
        edit_window.configure(bg="#34495E")

        tk.Label(edit_window, text="Edit Marks", font=("Arial", 14, "bold"), bg="#34495E", fg="white").pack(pady=10)

        tk.Label(edit_window, text="Test ID:", bg="#34495E", fg="white").pack()
        tk.Entry(edit_window, state="disabled", width=20).pack()
        tk.Label(edit_window, text="Student ID:", bg="#34495E", fg="white").pack()
        tk.Entry(edit_window, state="disabled", width=20).pack()
        tk.Label(edit_window, text="Subject ID:", bg="#34495E", fg="white").pack()
        tk.Entry(edit_window, state="disabled", width=20).pack()

        tk.Label(edit_window, text="Marks:", bg="#34495E", fg="white").pack()
        marks_entry = tk.Entry(edit_window, width=20)
        marks_entry.insert(0, marks)
        marks_entry.pack()

        def save_changes():
            new_marks = marks_entry.get()
            if not new_marks.isdigit():
                messagebox.showerror("Error", "Marks must be a number.")
                return

            update_student_marks(test_id, student_id, subject_id, int(new_marks))
            messagebox.showinfo("Success", "Marks updated successfully.")
            edit_window.destroy()
            self.view_update_marks()  # Refresh table

        tk.Button(edit_window, text="Save Changes", command=save_changes, bg="#27AE60", fg="white").pack(pady=10)

    def open_student_review(self):
        """Open the student review window by running studentReview.py."""
        script_path = os.path.abspath(r"C:\Users\Wathma\Desktop\MIT\Tuition management system Old - Copy\modules\studentReview.py")
        subprocess.Popen(["python", script_path])





# Example usage:
if __name__ == "__main__":
    teacher_id = 2  # Replace with actual logged-in teacher's ID
    app = TeacherDashboard(teacher_id)
    app.mainloop()
