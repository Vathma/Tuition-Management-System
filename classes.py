import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mysql.connector
import csv

# Connect to database
def connect():

    return mysql.connector.connect(
    host = "localhost",
    user = "rootap",
    password = "rootap123",
    database = "schooldb"
)

# Fetch classes from the database
def fetch_classes():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM class")  # Adjust based on actual table structure
    data = cursor.fetchall()
    conn.close()
    return data

# Function to refresh table data
def refresh_table(table, data):
    for row in table.get_children():
        table.delete(row)  # Clear existing data
    for row in data:
        table.insert("", tk.END, values=row)


# Function to sort columns
def sort_table(table, col, reverse):
    data = [(table.set(k, col), k) for k in table.get_children("")]
    data.sort(reverse=reverse)

    for index, (_, k) in enumerate(data):
        table.move(k, "", index)

    table.heading(col, command=lambda: sort_table(table, col, not reverse))

# Function to export table data to CSV
def export_to_csv(table):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Subject", "Teacher", "Class Days", "Allocate Class Room"])  # Header

            for row_id in table.get_children():
                writer.writerow(table.item(row_id)['values'])

        messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")

# Function to edit class details
def edit_class(table):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a class to edit.")
        return

    # Get selected class details
    class_details = table.item(selected_item)["values"]

    # Create Edit Window
    edit_window = tk.Toplevel()
    edit_window.title("Edit Class Details")
    edit_window.geometry("400x420")
    edit_window.resizable(False, False)
    edit_window.configure(bg="#1ABC9C")

    # Title Label
    title_label = tk.Label(
            edit_window,
            text="Edit Class Details",
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
    labels = ["ID", "Subject", "Teacher", "Class Days", "Allocate Class Room"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, bg="#E3F2FD").pack(pady=2)
        entry = tk.Entry(form_frame)
        entry.pack(pady=2)
        entry.insert(0, class_details[i])
        if label == "ID":
            entry.config(state="readonly")  # ID should not be editable
        entries[label] = entry

    # Save Button
    def save_changes():
        class_id = entries["ID"].get()
        subject = entries["Subject"].get()
        teacher = entries["Teacher"].get()
        days = entries["Class Days"].get()
        allocate_classroom = entries["Allocate Class Room"].get()

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE class 
            SET subject_id=%s, teacher_id=%s,  class_day=%s, classroom=%s 
            WHERE class_id=%s
        """, ( subject, teacher, days, allocate_classroom, class_id ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Class details updated successfully!")
        edit_window.destroy()
        refresh_table(table, fetch_classes())

    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.pack(pady=10)

def delete_class(table):
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


# Function to display class data
def view_classes():
    class_window = tk.Toplevel()
    class_window.title("View Classes")
    class_window.geometry("800x400")
    class_window.configure(bg="#1ABC9C")

        # Title
    tk.Label(class_window, text="Class List", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

    # Search Bar
    search_frame = tk.Frame(class_window, bg="#1ABC9C")
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Search by Subject::", bg="#1ABC9C", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 12))
    search_entry.pack(side=tk.LEFT, padx=5)

        # Function to search for classes based on subject
    def search_classes(table, subject):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM class WHERE subject_id LIKE %s", ('%' + subject + '%',))
        data = cursor.fetchall()
        conn.close()
        refresh_table(table, data)

    search_button = tk.Button(search_frame, text="Search", command=lambda: search_classes(class_table, search_entry.get()), bg="#3498DB", fg="white", font=("Arial", 10))
    search_button.pack(side=tk.LEFT, padx=5)
    
    # search_label = tk.Label(button_frame, text="Search by Subject:")
    # search_label.pack(side="left", padx=5)
    # search_entry = tk.Entry(button_frame)
    # search_entry.pack(side="left", padx=5)
    # search_button = tk.Button(button_frame, text="Search", command=lambda: search_classes(class_table, search_entry.get()))
    # search_button.pack(side="left", padx=5)

    # Define columns
    columns = ("ID", "Subject", "Teacher", "Class Days", "Allocate Class Room")

    # Create Treeview table
    class_table = ttk.Treeview(class_window, columns=columns, show="headings")
    
    # Add column headings with sorting
    for col in columns:
        class_table.heading(col, text=col, command=lambda _col=col: sort_table(class_table, _col, False))
        class_table.column(col, anchor="center", width=120)

    class_table.pack(expand=True, fill="both", pady=10)

    # Fetch and insert initial data
    refresh_table(class_table, fetch_classes())

    # Buttons Frame
    button_frame = tk.Frame(class_window, bg="#1ABC9C")
    button_frame.pack(pady=10)

    # Edit Button
    edit_button = tk.Button(button_frame, text="Edit Selected", command=lambda: edit_class(class_table), bg="#F39C12", fg="white")
    edit_button.pack(side="left", padx=5)

    # Delete Button
    delete_button = tk.Button(button_frame, text="Delete Selected", command=lambda: delete_class(class_table), bg="#E74C3C", fg="white")
    delete_button.pack(side="left", padx=5)

    # Refresh Button
    refresh_button = tk.Button(button_frame, text="Refresh", command=lambda: refresh_table(class_table, fetch_classes()),bg="#3498DB", fg="white")
    refresh_button.pack(side="left", padx=5)

    # Export Button
    export_button = tk.Button(button_frame, text="Export to CSV", command=lambda: export_to_csv(class_table),bg="#228B22", fg="white")
    export_button.pack(side="left", padx=5)

    tk.Button(button_frame, text="Close", command=class_window.destroy, bg="red", fg="white").pack(side=tk.LEFT, padx=5)



# Example button in Admin Dashboard to open View Classes window
def admin_dashboard():
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("400x300")

    tk.Button(root, text="View Classes", command=view_classes).pack(pady=20)

    root.mainloop()

# Run the Admin Dashboard (for testing)
if __name__ == "__main__":
    admin_dashboard()
