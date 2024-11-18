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
