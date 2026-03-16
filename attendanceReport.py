import mysql.connector
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import csv
from tkcalendar import DateEntry

# Function to get attendance records
def fetch_attendance(student_id=None):
    """Fetch attendance records from the database, optionally filtered by student ID."""
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="rootap",
            password="rootap123",
            database="schooldb"
        )
        cursor = db_connection.cursor()

        # Query to fetch attendance records
        if student_id:
            query = "SELECT attendance_id,student_id, class_id, attendance_status, date FROM attendance WHERE student_id = %s"
            cursor.execute(query, (student_id,))
        else:
            query = "SELECT attendance_id, student_id, class_id, attendance_status, date FROM attendance"
            cursor.execute(query)

        records = cursor.fetchall()
        cursor.close()
        db_connection.close()

        return records

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

# Function to display attendance records in the table
def show_attendance():
    """Fetch and display attendance records in the table."""
    student_id = student_id_var.get().strip()
    records = fetch_attendance(student_id if student_id else None)

    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    # Insert new records
    for record in records:
        tree.insert("", "end", values=record)

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

    for row in fetch_attendance():
        tree.insert("", tk.END, values=row)  # Reinsert updated data

        # Function to export table data to CSV
def export_to_csv(table):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Student ID", "Class ID", "Attendance Status", "Date"])  # Header

            for row_id in table.get_children():
                writer.writerow(table.item(row_id)['values'])

            messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")
        
        # Function to edit attendance details
def edit_attendance(table):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to edit.")
        return

    # Get selected attendance details
    attendance_details = table.item(selected_item)["values"]
    attendance_id = table.item(selected_item)["values"][0]  

    # Create Edit Window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Attendance Details")
    edit_window.geometry("400x420")
    edit_window.resizable(False, False)
    edit_window.configure(bg="#1ABC9C")

    # Title Label
    title_label = tk.Label(
            edit_window,
            text="Edit Attendance Details",
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
    labels = ["Student ID", "Class ID", "Attendance Status", "Date"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, bg="#E3F2FD").pack(pady=2)

        if label == "Attendance Status":
            #  Use dropdown for ENUM values
            entry = ttk.Combobox(form_frame, values=["Present", "Absent"], state="readonly")
            entry.set(attendance_details[i+1])  # Set current value

        elif label == "Date":
            #  Use DateEntry widget and ensure correct format
            entry = DateEntry(form_frame, date_pattern="yyyy-mm-dd")  
            entry.set_date(attendance_details[i+1])  # Set current value

        else:
            # Default Entry widget for Student ID & Class ID
            entry = tk.Entry(form_frame)
            entry.insert(0, attendance_details[i+1])
            if label == "Student ID":
                entry.config(state="readonly")  # Make ID non-editable

        entry.pack(pady=2)
        entries[label] = entry

    # Save Button
    def save_changes():
        student_id = entries["Student ID"].get()
        classN = entries["Class ID"].get()
        attenS = entries["Attendance Status"].get()
        dateI = entries["Date"].get()  # Ensure it's in 'YYYY-MM-DD' format

        print(f"Updating ID: {attendance_id}, Student ID: {student_id}, Class ID: {classN}, Status: {attenS}, Date: {dateI}")  #  Debug print

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="rootap",
                password="rootap123",
                database="schooldb"
            )
            cursor = conn.cursor()

            sql = """
                UPDATE attendance 
                SET student_id = %s, class_id = %s, attendance_status = %s, date = %s
                WHERE attendance_id = %s
            """
            values = (student_id, classN, attenS, dateI, attendance_id)

            cursor.execute(sql, values)
            conn.commit()

            if cursor.rowcount == 0:  #  Check if any row was updated
                messagebox.showerror("Update Failed", "No records were updated. Check if the ID exists.")
            else:
                messagebox.showinfo("Success", "Attendance details updated successfully!")

            conn.close()
            edit_window.destroy()
            # refresh_table(table)  #  Refresh table after update

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    # button_frame = tk.Frame(root, bg="#1ABC9C")
    # button_frame.pack(pady=10)

    tk.Button(edit_window, text="Save", command=save_changes, bg="#E3F2FD").pack(pady=10)


def delete_attendance(table):
            selected_item = table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a record to delete.")
                return

            attendance_id = table.item(selected_item)["values"][0]  # Get ID

            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Attendance ID {attendance_id}?")
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
                cursor.execute("DELETE FROM attendance WHERE attendance_id = %s", (attendance_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "attendance record deleted successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete attendance record: {e}")    

# GUI Setup
root = tk.Tk()
root.title("Student Attendance Report")
root.geometry("750x400")
root.configure(bg="#1ABC9C")

# Title
tk.Label(root, text="Student Attendance Report", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

# Search Bar
search_frame = tk.Frame(root, bg="#1ABC9C")
search_frame.pack(pady=5)

# Input for Student ID (Optional)
tk.Label(search_frame, text="Enter Student ID (Optional):", bg="#1ABC9C", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
student_id_var = tk.StringVar()
tk.Entry(search_frame, textvariable=student_id_var, font=("Arial", 12)).pack(side=tk.LEFT,pady=5)

# Button to fetch attendance
tk.Button(search_frame, text="Show Attendance", command=show_attendance, bg="#3498DB", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

# Table for displaying attendance records
columns = ("Attendance ID","Student ID", "Class ID", "Attendance Status", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    if col == "Attendance ID":
        tree.column(col, width=0, stretch=False)  #  Hide Attendance ID
    else:
        tree.column(col, anchor="center", width=120)

tree.pack(expand=True, fill="both")

button_frame = tk.Frame(root, bg="#1ABC9C")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Edit Selected", command=lambda: edit_attendance(tree), bg="#F39C12", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete Selected", command=lambda: delete_attendance(tree), bg="#E74C3C", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Export to CSV", command=lambda: export_to_csv(tree), bg="#228B22", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Refresh", command=lambda: refresh_table(tree), bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Close", command=root.destroy, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

root.mainloop()
