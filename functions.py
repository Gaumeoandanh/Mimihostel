import re

# Generate ID like "BKG-0001"
def generate_booking_id(index):
    return f"BKG-{index + 1:04d}"

# Function to validate email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)
