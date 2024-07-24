import streamlit as st
import sqlite3

# Initialize the database and create tables if not exist
def init_db():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Create employees table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        role TEXT NOT NULL,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
    ''')

    # Create departments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        manager_id INTEGER,
        FOREIGN KEY (manager_id) REFERENCES employees(id)
    )
    ''')

    # Create issue_logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS issue_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        department_id INTEGER NOT NULL,
        issue_description TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
    ''')

    # Insert initial manager if not exists
    cursor.execute('''
    INSERT INTO employees (name, email, age, gender, role) 
    SELECT 'Satish G', 'satish.g@goml.io', 40, 'Male', 'Manager'
    WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email='satish.g@goml.io')
    ''')

    # Get the manager's id
    cursor.execute("SELECT id FROM employees WHERE email='satish.g@goml.io'")
    manager_id = cursor.fetchone()[0]

    # Insert department with the manager
    cursor.execute('''
    INSERT INTO departments (name, manager_id)
    SELECT 'Engineering', ?
    WHERE NOT EXISTS (SELECT 1 FROM departments WHERE name='Engineering')
    ''', (manager_id,))

    # Update manager's department_id
    cursor.execute('''
    UPDATE employees SET department_id = (SELECT id FROM departments WHERE name='Engineering') WHERE email='satish.g@goml.io'
    ''')

    conn.commit()
    conn.close()

# Call the init_db function to initialize the database
init_db()

# Main application
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Employee Onboarding", "Employee Support", "Admin"])


if __name__ == "__main__":
    main()
