import mysql.connector
import tkinter as tk
from tkinter import ttk,filedialog
import csv
from tkinter import messagebox

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="rootap",
        password="rootap123",
        database="schooldb"
    )

def fetch_users():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch users: {e}")
        return []


users = fetch_users()

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

            for row in fetch_users():
                tree.insert("", tk.END, values=row)  # Reinsert updated data

        # Function to export table data to CSV
def export_to_csv(table):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["User ID", "Username", "Password","Role","Created at","Updated at"])  # Header

                    for row_id in table.get_children():
                        writer.writerow(table.item(row_id)['values'])

                messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")
        
        # Function to edit teacher details
def edit_user(table):
            selected_item = table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a user to edit.")
                return

            # Get selected teacher details
            user_details = table.item(selected_item)["values"]
            user_role = user_details[3]

            # Create Edit Window
            edit_window = tk.Toplevel()
            edit_window.title("Edit User Details")
            edit_window.geometry("400x420")
            edit_window.resizable(False, False)
            edit_window.configure(bg="#1ABC9C")

            # Title Label
            title_label = tk.Label(
                    edit_window,
                    text="Edit User Details",
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
            labels = ["User ID","Username", "Password","Role","Created at","Updated at"]
            entries = {}

            for i, label in enumerate(labels):
                tk.Label(form_frame, text=label,bg="#E3F2FD").pack(pady=2)
                entry = tk.Entry(form_frame)
                entry.pack(pady=2)
                entry.insert(0, user_details[i])
                if label in ["User ID", "Username","Role"]:
                    entry.config(state="readonly")   # ID should not be editable
                entries[label] = entry
                if user_role == "admin" and label != "Password":
                    entry.config(state="readonly")

            # Save Button
            def save_changes():
                user_id = entries["User ID"].get()
                uName = entries["Username"].get()
                passw = entries["Password"].get()
                # createdAt = entries["Created at"].get()
                # updatedAt = entries["Updated at"].get()
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
                    UPDATE user 
                    SET username=%s, password=%s
                    WHERE user_id=%s
                """, ( uName,  passw, user_id ))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "User details updated successfully!")
                edit_window.destroy()
                # refresh_table(table, fetch_user())

            tk.Button(edit_window, text="Save", command=save_changes, bg="green", fg="white").pack(pady=10)   

def delete_user(table):
            selected_item = table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a user to delete.")
                return

            user_id = table.item(selected_item)["values"][0]  # Get Teacher ID

            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete user ID {user_id}?")
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
                cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "User deleted successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete User: {e}")    


# """Create a window to display Teacher data in a table format."""
root = tk.Tk()
# users_window = tk.Toplevel(root)
users_window = tk.Toplevel(root)
users_window.title("View Users")
users_window.geometry("750x400")
users_window.configure(bg="#1ABC9C")

# Title
tk.Label(users_window, text="Users", font=("Arial", 16, "bold"), bg="#1ABC9C", fg="white").pack(pady=10)

# Search Bar
search_frame = tk.Frame(users_window, bg="#1ABC9C")
search_frame.pack(pady=5)

tk.Label(search_frame, text="Search:", bg="#1ABC9C", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
search_entry = tk.Entry(search_frame, font=("Arial", 12))
search_entry.pack(side=tk.LEFT, padx=5)
        
def search():
    query = search_entry.get().lower()
    tree.selection_remove(tree.selection())  # Clear previous selection
    for row in tree.get_children():
        values = tree.item(row)["values"]
        if any(str(val).lower().startswith(query) for val in values):
            tree.selection_set(row)

search_button = tk.Button(search_frame, text="Search", command=search, bg="#3498DB", fg="white", font=("Arial", 10))
search_button.pack(side=tk.LEFT, padx=5)

    # Table (Treeview)
columns = ("User ID", "Username", "Password","Role","Created at","Updated at")
tree = ttk.Treeview(users_window, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col, command=lambda col=col: sort_column(tree, col, False)) # Sortable columns
    tree.column(col, width=100, anchor="center")

        # Insert data into table
for row in users:
    tree.insert("", tk.END, values=row)

    tree.pack(pady=10, fill="both", expand=True)

button_frame = tk.Frame(users_window, bg="#1ABC9C")
button_frame.pack(pady=10)

def close_window():
    users_window.destroy()  # Close the create user window
    root.destroy()

tk.Button(button_frame, text="Edit Selected", command=lambda: edit_user(tree), bg="#F39C12", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete Selected", command=lambda: delete_user(tree), bg="#E74C3C", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Export to CSV", command=lambda: export_to_csv(tree), bg="#228B22", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Refresh", command=lambda: refresh_table(tree), bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Close", command=close_window, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

root.withdraw()

root.mainloop()