import streamlit as st
import gspread
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

# Function to connect to Google Sheets
def connect_to_google_sheet():
    # Load the service account key from the environment variable
    if not st.secrets.connections.gsheets:
        raise ValueError("Please config connections.gsheets.")

    credentials = {
        "spreadsheet": st.secrets.connections.gsheets.spreadsheet,
        "worksheet": st.secrets.connections.gsheets.worksheet,
        "type": st.secrets.connections.gsheets.type,
        "project_id": st.secrets.connections.gsheets.project_id,
        "private_key_id": st.secrets.connections.gsheets.private_key_id,
        "private_key": st.secrets.connections.gsheets.private_key,
        "client_email": st.secrets.connections.gsheets.client_email,
        "client_id": st.secrets.connections.gsheets.client_id,
        "auth_uri": st.secrets.connections.gsheets.auth_uri,
        "token_uri": st.secrets.connections.gsheets.token_uri,
        "auth_provider_x509_cert_url": st.secrets.connections.gsheets.auth_provider_x509_cert_url,
        "client_x509_cert_url": st.secrets.connections.gsheets.client_x509_cert_url,
        "universe_domain": st.secrets.connections.gsheets.universe_domain,
    }

    client = gspread.service_account_from_dict(credentials)

    # Open the spreadsheet by URL
    sheet = client.open_by_url(st.secrets.connections.gsheets.spreadsheet)
    return sheet.worksheet("Booking")  # Open the Booking sheet