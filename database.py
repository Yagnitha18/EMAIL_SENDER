#DATABASE.PY
import psycopg2
from config import DB_CONFIG

def get_db_connection():
    return psycopg2.connect(
        host=DB_CONFIG['host'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )

def insert_email_status(email, status, delivery_status='Pending', opened=False):
    """
    Insert a new email status into the database.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO email1 (email, status, delivery_status, opened) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (email, status, delivery_status, opened)
                )
                conn.commit()
                print(f"Inserted status for email: {email}")
    except Exception as e:
        print(f"Error inserting email status: {e}")



def update_email_status(email, status, delivery_status=None, opened=None):
    # Build the query dynamically based on the provided arguments
    query = "UPDATE email1 SET "
    values = []

    # Check which fields need to be updated and build the SET clause dynamically
    if status:
        query += "status = %s, "
        values.append(status)
    if delivery_status:
        query += "delivery_status = %s, "
        values.append(delivery_status)
    if opened is not None:
        query += "opened = %s, "
        values.append(opened)

    # Remove trailing comma and space
    query = query.rstrip(", ")

    # Add the condition to target the specific email
    query += " WHERE email = %s"
    values.append(email)

    # Execute the query
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, tuple(values))
                conn.commit()  # Commit the transaction
                print(f"Updated email status for {email}")
    except Exception as e:
        print(f"Error updating email status: {e}")
def get_email_status():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT status, delivery_status, COUNT(*) 
                FROM email1 
                GROUP BY status, delivery_status
            """)
            return dict(cursor.fetchall())
def get_email_count_by_status():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Query to count emails by status and delivery status
                cursor.execute("""
                    SELECT status, 
                           delivery_status, 
                           COUNT(*) 
                    FROM email1 
                    GROUP BY status, delivery_status
                """)
                result = cursor.fetchall()

                # Initialize counters
                email_counts = {
                    'Sent': 0,
                    'Delivered': 0,
                    'Failed': 0,
                    'Opened': 0,
                    'Total': 0
                }

                # Process the result
                for row in result:
                    status = row[0]
                    delivery_status = row[1]
                    count = row[2]

                    # Increment counts based on status and delivery_status
                    if status == 'Sent':
                        email_counts['Sent'] += count
                    if delivery_status == 'Delivered':
                        email_counts['Delivered'] += count
                    if status == 'Failed':
                        email_counts['Failed'] += count
                    if status == 'Opened':
                        email_counts['Opened'] += count
                    # Increment total count
                    email_counts['Total'] += count

                return email_counts

    except Exception as e:
        print(f"Error retrieving email counts by status: {e}")
        return {
            'Sent': 0,
            'Delivered': 0,
            'Failed': 0,
            'Opened': 0,
            'Total': 0
        }

