# CUSTOM EMAIL SENDER
This project is a Flask-based email automation application with Celery for background task management, PostgreSQL for data persistence, and SMTP for email sending. It supports features such as CSV-based email generation, scheduling with throttling, and tracking email statuses.

---

## Features
- Upload CSV files for bulk email data.
- Generate emails using default or custom templates.
- Schedule emails with batch size and interval options.
- Monitor email statuses in real-time.
- Easy-to-configure database and SMTP settings.

---

## Prerequisites
1. Python 3.8 or later.
2. PostgreSQL installed and running.
3. Redis server for Celery.
4. An SMTP server for sending emails (e.g., Gmail SMTP).

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Yagnitha18/EMAIL_SENDER.git
cd EMAIL_SENDER
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
```
### 3. Activate the Virtual Environment
```bash
venv\Scripts\activate
```
### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Configure the Database
1. Create a PostgreSQL database:
   ```bash
   CREATE DATABASE emailsender;
   ```
2. Update config.py with your PostgreSQL credentials:
   ```bash
   DB_CONFIG = {
    'host': 'localhost',
    'database': 'emailsender',
    'user': '<your-postgres-username>',
    'password': '<your-postgres-password>',
    'port': 5432
   }
   ```
3. Create the email1 table in your database:
   ```bash
   CREATE TABLE email1 (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    delivery_status VARCHAR(50),
    opened BOOLEAN DEFAULT FALSE
   );
   ```
### 6. Configure SMTP
Update the SMTP_CONFIG in config.py with your email credentials:
```bash
SMTP_CONFIG = {
    'email': '<your-email>',
    'password': '<your-email-app-password>',
    'server': 'smtp.gmail.com',
    'port': 587
}
```
### 7. Start Redis Server
Ensure Redis is running. If not, start it:
```bash
redis-server
```
### 8.  Start Celery Worker
Open a new terminal and run:
```bash
celery -A celery_app worker --pool=solo --loglevel=info
```
### 9. Run the Flask Application
Run the application using:
```bash
python app.py
```
The application will be available at http://127.0.0.1:5000.

## Usage Instructions
Upload CSV
1. Access the dashboard at http://127.0.0.1:5000.
2. Upload a CSV file with the necessary fields (e.g., First Name, Email, Company Name, etc.).

## Generate Emails
1. Enter a custom template or use the default templates.
2. Click "Generate Emails" to preview the generated emails.

## Schedule Emails
1. Set the schedule time, batch size, and interval in the form.
2. Click "Schedule Emails" to start email sending.

## Monitor Email Statuses
The email statuses (e.g., Sent, Failed, Delivered, Opened) are displayed in real-time on the dashboard.

## Directory Structure
```bash
├── app.py              # Main Flask application
├── celeryapp.py        # Celery task definitions
├── config.py           # Configuration settings (DB, SMTP)
├── database.py         # Database utility functions
├── email_utils.py      # Email generation and sending utilities
├── static/css/style.css # CSS for the dashboard
├── templates/
│   └── dashboard.html  # HTML template for the dashboard
├── uploads/            # Directory to store uploaded CSV files
└── requirements.txt    # Python dependencies
```

## Dependencies
- Flask
- Pandas
- Celery
- Redis
- psycopg2
- smtplib

## Contribution
Feel free to open issues or submit pull requests to improve this project.

## License
This project is licensed under the MIT License.
Replace <your-username> and <your-repository-name> with your GitHub username and repository name before adding this file to your repository. Save this content as README.md in the root directory of your project.
