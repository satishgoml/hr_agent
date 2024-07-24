import streamlit as st
import sqlite3
import pandas as pd

# Function to get departments for the dropdown
def get_departments():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM departments')
    departments = cursor.fetchall()
    conn.close()
    return departments

# Function to get employees filtered by department
def get_employees(department_id=None):
    conn = sqlite3.connect('employees.db')
    query = 'SELECT * FROM employees'
    params = ()
    if department_id:
        query += ' WHERE department_id = ?'
        params = (department_id,)
    conn.row_factory = sqlite3.Row  # Enable row factory to get column names
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Function to get issue logs filtered by department
def get_issue_logs(department_id=None):
    conn = sqlite3.connect('employees.db')
    query = '''
    SELECT il.id, e.name AS employee_name, il.issue_description, il.timestamp
    FROM issue_logs il
    JOIN employees e ON il.employee_id = e.id
    '''
    params = ()
    if department_id:
        query += ' WHERE e.department_id = ?'
        params = (department_id,)
    conn.row_factory = sqlite3.Row  # Enable row factory to get column names
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Admin Page
def admin():
    st.title("Admin Dashboard")

    # Department filter
    departments = get_departments()
    department_options = {f"{name} (ID: {id})": id for id, name in departments}
    selected_department = st.selectbox("Filter by Department", list(department_options.keys()) + ["All"])

    department_id = None
    if selected_department != "All":
        department_id = department_options[selected_department]

    # Display employees based on department filter
    st.subheader("Employee List")
    employees_df = get_employees(department_id)
    if not employees_df.empty:
        st.dataframe(employees_df)

        # Add delete button for each row
        for index, row in employees_df.iterrows():
            col1, *cols, col_last = st.columns([1] + [2] * (len(employees_df.columns) - 1) + [2])
            col1.text(row[employees_df.columns[0]])  # ID column
            for col, column_name in zip(cols, employees_df.columns[1:]):
                col.text(row[column_name])
            with col_last:
                delete_button = st.button("Delete", key=row[employees_df.columns[0]])

            if delete_button:
                delete_employee(row[employees_df.columns[0]])
                st.experimental_rerun()
    else:
        st.write("No employees found for the selected department.")

    # Display issue logs based on department filter
    st.subheader("Issue Logs")
    logs_df = get_issue_logs(department_id)
    if not logs_df.empty:
        st.dataframe(logs_df)
    else:
        st.write("No issue logs found for the selected department.")

def delete_employee(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
    conn.commit()
    conn.close()
    st.success(f"Employee with ID {employee_id} has been deleted.")

admin()
