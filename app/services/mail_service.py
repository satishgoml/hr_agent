import requests

class EmailSender:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def send_email(self, receiver_emails, subject, body):
        endpoint = f"{self.api_base_url}/send_email/"
        payload = {
            "receiver_emails": receiver_emails,
            "subject": subject,
            "body": body
        }
        
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print(f"Email sent successfully! Status code: {response.status_code}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

# Example usage
if __name__ == "__main__":
    api_base_url = "http://54.84.189.207"  # Base URL of the API
    email_sender = EmailSender(api_base_url)
    
    receiver_emails = ["new.employee@example.com"]
    subject = "Welcome to the Company!"
    body = """
    Welcome to the team!

    Here are some important resources to get you started:

    - [Slack Invite](https://slack.com/invite-link)
    - [Employee Policy Document](https://example.com/employee-policy)

    Please reach out if you have any questions.

    Best,
    HR Team
    """
    
    email_sender.send_email(receiver_emails, subject, body)
