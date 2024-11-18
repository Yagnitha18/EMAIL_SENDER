import smtplib
from email.mime.text import MIMEText
from database import insert_email_status,get_db_connection
import random
import logging

# Define email templates
TEMPLATES = [
    "Hello {First Name},\n\nWe at {Company Name} are thrilled to introduce {Product Name} in {Location}. It’s designed to meet your needs and exceed expectations.\n\nLet us know if you’d like more details.\n\nBest,\nThe Team",
    "Hi {First Name},\n\nWe hope this message finds you well! {Company Name} is excited to bring {Product Name} to {Location}. We’d love to schedule a call to discuss how it can benefit you.\n\nBest regards,\nYour Sales Team",
    "Dear {First Name},\n\n{Company Name} is excited to announce {Product Name} in {Location}. It's built to enhance your experience and provide value. Reach out for more details!\n\nWarm regards,\n{Company Name} Team"
]

def generate_email_content(row_data):
    """
    Generate email content using a predefined template.
    """
    try:
        # Choose a random template
        template = random.choice(TEMPLATES)
       # Fill in the placeholders with row data
        return template.format(**row_data)
    except KeyError as e:
        raise ValueError(f"Missing key {e} in row data.") from e

def send_email(to_email, subject, content, smtp_config):
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = smtp_config['email']
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
            server.starttls()
            server.login(smtp_config['email'], smtp_config['password'])
            server.send_message(msg)
            logging.info(f"Email successfully sent to {to_email}.")
    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {e}", exc_info=True)
        raise
