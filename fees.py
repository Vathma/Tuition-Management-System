# modules/fees.py
import mysql.connector
from database.db_setup import connect

def add_fee_payment(student_id, amount, payment_date):
    """Record a fee payment made by a student."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Fees (student_id, amount, payment_date) VALUES (?, ?, ?)",
        (student_id, amount, payment_date)
    )
    conn.commit()
    conn.close()

def get_student_balance(student_id):
    """Calculate the total balance for a student."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(amount) FROM Fees WHERE student_id = ?",
        (student_id,)
    )
    total_paid = cursor.fetchone()[0] or 0
    conn.close()

    # Assuming a constant fee amount per student; you can adjust as needed
    total_fees_due = 1000  # Example fee amount
    return total_fees_due - total_paid

def generate_receipt(student_id):
    """Generate a payment receipt for a student."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT student_id, amount, payment_date FROM Fees WHERE student_id = ? ORDER BY payment_date DESC",
        (student_id,)
    )
    payments = cursor.fetchall()
    conn.close()

    receipt = f"Receipt for Student ID {student_id}\n"
    receipt += "Date       | Amount\n"
    receipt += "-" * 20 + "\n"

    for payment in payments:
        receipt += f"{payment[2]} | ${payment[1]:.2f}\n"

    return receipt
