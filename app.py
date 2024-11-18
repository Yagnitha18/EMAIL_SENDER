import os
import pandas as pd
from flask import Flask, request, render_template, jsonify
from celeryapp import schedule_emails
from database import get_email_status,get_email_count_by_status
from email_utils import generate_email_content
from datetime import datetime
from pytz import timezone


app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def load_data():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

    secure_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        file.save(secure_path)
    except Exception as e:
        return jsonify({"error": f"Error saving file: {e}"}), 500

    return jsonify({"status": "Data loaded successfully", "path": secure_path})

@app.route('/generate_emails', methods=['POST'])
def generate_emails():
    """
    Generate email previews using a user-defined template or default templates.
    """
    try:
        # Read the uploaded CSV file
        csv_path = os.path.join(UPLOAD_FOLDER, 'data.csv')
        data = pd.read_csv(csv_path)
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {e}"}), 400

    try:
        # Parse the custom template from the request
        request_data = request.get_json()
        custom_template = request_data.get('template')

        # Generate email content for each row
        messages = []
        for _, row in data.iterrows():
            row_data = row.to_dict()
            if custom_template:
                # Use the custom template
                try:
                    email_content = custom_template.format(**row_data)
                except KeyError as e:
                    return jsonify({"error": f"Missing placeholder {e} in row data."}), 400
            else:
                # Use default template
                email_content = generate_email_content(row_data)

            messages.append(email_content)

        return jsonify({"messages": messages})
    except Exception as e:
        return jsonify({"error": f"Error generating emails: {e}"}), 500


@app.route('/schedule_emails', methods=['POST'])
def schedule_emails_route():
    """
    Schedule emails for sending using Celery with scheduling and throttling options.
    """
    try:
        data = pd.read_csv(os.path.join(UPLOAD_FOLDER, 'data.csv')).to_dict(orient='records')
        params = request.get_json()

        # Extract scheduling and throttling options
        schedule_time = params.get('scheduleTime')  # Expecting ISO format datetime string
        batch_size = int(params.get('batchSize', 50))  # Default to 50 emails per batch
        interval = int(params.get('interval', 60))  # Default to 60 minutes between batches

        # Validate and convert schedule_time to datetime
        if schedule_time:
            if isinstance(schedule_time, str):  # If it's an ISO 8601 datetime string
                try:
                    # Try parsing the string as a datetime object (with timezone awareness)
                    utc_schedule_time = datetime.fromisoformat(schedule_time).astimezone(timezone('UTC'))
                except ValueError:
                    return jsonify({"error": "Invalid ISO 8601 datetime format for scheduleTime."}), 400
            else:
                return jsonify({"error": "scheduleTime must be a string in ISO 8601 format."}), 400
        else:
            utc_schedule_time = None  # No schedule time, so run immediately

        # Schedule the Celery task
        schedule_kwargs = {
            'data': data,
            'batch_size': batch_size,
            'interval': interval
        }

        # If schedule_time is provided, use ETA (estimated time of arrival)
        if schedule_time:
            schedule_emails.apply_async(kwargs=schedule_kwargs, eta=utc_schedule_time)
        else:
            schedule_emails.apply_async(kwargs=schedule_kwargs)

        return jsonify({"status": "Emails scheduled successfully."})

    except Exception as e:
        return jsonify({"error": f"Error scheduling emails: {e}"}), 400

@app.route('/analytics', methods=['GET'])
def get_email_statuses():
    try:
        # Get counts for each status
        email_statuses = get_email_count_by_status()
        return jsonify(email_statuses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)