import streamlit as st
import sqlite3
from services.mail_service import EmailSender

# Function to get department and manager based on employee ID
def get_department_and_manager(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Get department_id of the employee
    cursor.execute('''
    SELECT department_id FROM employees WHERE id = ?
    ''', (employee_id,))
    department_id = cursor.fetchone()
    if not department_id:
        conn.close()
        return None, None

    department_id = department_id[0]

    # Get manager's email for the department
    cursor.execute('''
    SELECT e.email FROM employees e
    JOIN departments d ON e.id = d.manager_id
    WHERE d.id = ?
    ''', (department_id,))
    manager_email = cursor.fetchone()
    conn.close()

    if manager_email:
        return department_id, manager_email[0]
    return department_id, None

# Function to get a list of employees
def get_employees():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM employees')
    employees = cursor.fetchall()
    conn.close()
    return employees

# Function to log issues in the database
def log_issue(employee_id, department_id, issue_description):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO issue_logs (employee_id, department_id, issue_description)
    VALUES (?, ?, ?)
    ''', (employee_id, department_id, issue_description))
    conn.commit()
    conn.close()

# Employee Support Page
def employee_support():
    st.title("Employee Support")

    # Get employees for the dropdown
    employees = get_employees()
    employee_options = {f"{name} (ID: {id})": id for id, name in employees}

    # Collect issue details
    with st.form("support_form"):
        selected_employee = st.selectbox("Select Employee", list(employee_options.keys()))
        issue_description = st.text_area("Describe your issue")
        submit_button = st.form_submit_button("Submit Issue")

        if submit_button:
            employee_id = employee_options[selected_employee]
            st.spinner("Processing...")

            # Get department and manager email
            department_id, manager_email = get_department_and_manager(employee_id)

            if manager_email:
                # Log the issue
                log_issue(employee_id, department_id, issue_description)

                # Notify department manager
                email_sender = EmailSender("http://54.84.189.207")
                issue_email_body = f"""
                The following issue was reported by employee ID {employee_id}:

                {issue_description}
                """
                try:
                    email_sender.send_email([manager_email], "Employee Issue Reported", issue_email_body)
                    st.success("Issue reported and department manager notified successfully!")
                except Exception as e:
                    st.error("Failed to notify department manager.")
            else:
                st.error("Failed to find the manager for the selected employee.")

employee_support()
