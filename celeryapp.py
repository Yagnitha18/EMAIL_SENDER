from celery import Celery
from email_utils import generate_email_content, send_email
from config import SMTP_CONFIG  # Import SMTP configuration
import logging
import time
from database import update_email_status,insert_email_status

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task(bind=True, max_retries=3)
def schedule_emails(self, data, batch_size=50, interval=60):
    """
    Schedule and throttle email sending using SMTP configuration.

    Args:
        data (list): List of dictionaries, each containing email details.
        batch_size (int): Number of emails to send in one batch.
        interval (int): Time (in minutes) to wait between batches.
    """
    try:
        logging.info(f"Starting email scheduling with batch_size={batch_size}, interval={interval} minutes.")

        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]  # Get the current batch

            for row in batch:
                email = row.get('Email')
                try:
                    insert_email_status(email,status = "Pending")
                    email_content = generate_email_content(row)  # Generate email content for the row
                    if email_content:
                        send_email(
                            to_email=email,
                            subject="Exciting Update!",
                            content=email_content,
                            smtp_config=SMTP_CONFIG  # Pass SMTP configuration dynamically
                        )
                        update_email_status(email, "Sent", delivery_status="Delivered", opened=False)
                        logging.info(f"Email sent to {row['Email']}.")
                except Exception as email_error:
                    update_email_status(email, "Failed", delivery_status="Failed", opened=False)
                    logging.error(f"Failed to send email to {row['Email']}: {email_error}", exc_info=True)

            # Throttle: Wait for the specified interval before sending the next batch
            if i + batch_size < len(data):
                logging.info(f"Throttling: Waiting for {interval} minutes before sending the next batch.")
                time.sleep(interval * 60)  # Convert minutes to seconds

    except Exception as e:
        logging.error(f"Error in email scheduling: {e}", exc_info=True)
        self.retry(exc=e, countdown=60)
