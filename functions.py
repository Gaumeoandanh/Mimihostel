import random
import smtplib
import json
from email.mime.text import MIMEText

def generate_booking_number():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

def send_otp_email(email, otp):
    msg = MIMEText(f"Your OTP for Mimihostel booking is: {otp}")
    msg['Subject'] = 'Mimihostel Booking OTP'
    msg['From'] = 'noreply@mimihostel.com'
    msg['To'] = email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('noreply@mimihostel.com', 'your_email_password')
    server.send_message(msg)
    server.quit()

def save_booking_data(booking_data):
    with open('db/bookings.json', 'w') as f:
        json.dump(booking_data, f)

def load_booking_data():
    try:
        with open('db/bookings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []