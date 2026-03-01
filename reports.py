# reports.py
import smtplib
from email.mime.text import MIMEText
from grading import view_student_grades
from attendance import view_student_attendance

def send_report_to_parent(student_id, parent_email):
    grades = view_student_grades(student_id)
    attendance = view_student_attendance(student_id)
    report_content = f"Grades: {grades}\nAttendance: {attendance}"

    msg = MIMEText(report_content)
    msg['Subject'] = "Student Report"
    msg['From'] = "your_email@example.com"
    msg['To'] = parent_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("your_email@example.com", "yourpassword")
        server.sendmail("your_email@example.com", parent_email, msg.as_string())
