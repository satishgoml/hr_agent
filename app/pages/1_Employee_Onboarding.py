import streamlit as st
import sqlite3
from services.mail_service import EmailSender
from services.social_media_service import SocialMediaPoster

# Function to add a new employee to the database
def add_employee(name, email, age, gender, role, department_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO employees (name, email, age, gender, role, department_id)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, age, gender, role, department_id))
    conn.commit()
    conn.close()

# Function to fetch departments and roles from the database
def get_departments():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM departments')
    departments = cursor.fetchall()
    conn.close()
    return departments

def get_roles():
    # This should ideally fetch roles from a defined list or a separate table if applicable.
    return ["Manager", "Developer", "Analyst", "Designer"]

def get_manager_email(department_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT e.email
    FROM employees e
    JOIN departments d ON e.id = d.manager_id
    WHERE d.id = ?
    ''', (department_id,))
    manager_email = cursor.fetchone()
    conn.close()
    return manager_email[0] if manager_email else None

# Onboarding Page
def onboarding():
    st.title("Employee Onboarding")

    # Collect employee details
    with st.form("onboarding_form"):
        name = st.text_input("Employee Name")
        email = st.text_input("Employee Email")
        age = st.number_input("Employee Age", min_value=18, max_value=100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        # Fetch departments and roles
        departments = get_departments()
        department_options = {name: id for id, name in departments}
        department_name = st.selectbox("Department", list(department_options.keys()))
        department_id = department_options[department_name]

        roles = get_roles()
        role = st.selectbox("Role", roles)

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            with st.spinner("Processing..."):
                add_employee(name, email, age, gender, role, department_id)
                st.success("Employee details saved.")

                # Send welcome email
                email_sender = EmailSender("http://54.84.189.207")
                welcome_email_body = f"""
                Welcome to the team, {name}!

                Here are some important resources to get you started:

                - [Slack Invite](https://slack.com/invite-link)
                - [Employee Policy Document](https://example.com/employee-policy)

                Best,
                HR Team
                """
                try:
                    email_sender.send_email([email], "Welcome to the Company!", welcome_email_body)
                    st.success("Welcome email sent successfully!")
                except Exception as e:
                    st.error("Failed to send welcome email.")

                # Notify department manager
                manager_email = get_manager_email(department_id)
                if manager_email:
                    manager_email_body = f"Please welcome our new employee, {name}, to your department."
                    try:
                        email_sender.send_email([manager_email], "New Employee Onboarding", manager_email_body)
                        st.success("Notification to department manager sent successfully!")
                    except Exception as e:
                        st.error("Failed to notify department manager.")
                else:
                    st.error("Failed to find manager for the selected department.")

                # Post to social media
                social_media_poster = SocialMediaPoster("http://54.84.189.207")
                post_title = f"Welcome {name}!"
                post_image_url = "https://example.com/welcome-image.png"
                post_text_content = f"We're excited to welcome {name} to our team!"
                try:
                    social_media_poster.post_linkedin(post_title, post_image_url, post_text_content)
                    st.success("Social media announcement posted successfully!")
                except Exception as e:
                    st.error("Failed to post social media announcement.")

                st.success("Onboarding process completed!")

onboarding()
