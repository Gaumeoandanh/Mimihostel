import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import json
from google.oauth2 import service_account

if st.button("Back"):
    st.switch_page(page='pages/home.py')

# Function to connect to Google Sheets
def connect_to_google_sheet():
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Load environment variables from .env file (located in the same directory)
    load_dotenv()

    # Load the service account key from the environment variable
    # service_account_info = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
    service_account_info = str(st.secrets["GOOGLE_SERVICE_ACCOUNT_KEY"])
    if not service_account_info:
        raise ValueError("Environment variable GOOGLE_SERVICE_ACCOUNT_KEY is not set.")

    # Convert all single quotes to double quotes in the service account info
    service_account_info = service_account_info.replace("'", '"')
    
    # Parse the JSON string
    # service_account_json = json.loads(service_account_info)
    try:
        service_account_json = json.loads(service_account_info)
    except Exception as e:
        st.error(f"Huhu! An error occurred: {e}")

    # Authenticate using the service account information
    #credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_json, scope)
    credentials = service_account.Credentials.from_service_account_info(service_account_json, scopes=scope)
    client = gspread.authorize(credentials)

    # Open the spreadsheet by URL
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1vZwEGVZnsDYtBGGfoOrN23qSjulRfrzWA4dmhAF1Q1M/edit?usp=sharing")
    return sheet.worksheet("Booking")  # Open the Booking sheet

# Function to find a booking by Booking ID and Name
def find_booking(booking_id, name):
    sheet = connect_to_google_sheet()
    records = sheet.get_all_records()  # Get all records from the sheet

    for record in records:
        if record.get("Booking ID") == booking_id and record.get("Your Name") == name:
            return record  # Return the matching record
    
    return None  # Return None if no match is found

# Streamlit app for the Inquiry Page
st.title("Reservation Inquiry Service", anchor=False)

# Input form
with st.form("inquiry_form"):
    booking_id = st.text_input("Booking ID (*)")
    name = st.text_input("Your Name (*)")

    # Inquiry button
    inquiry_submitted = st.form_submit_button("Inquiry", use_container_width=True)

if inquiry_submitted:
    if not booking_id or not name:
        st.error("Both Booking ID and Your Name are required!")
    else:
        # Lookup booking information
        try:
            record = find_booking(booking_id, name)

            if record:
                # Display the booking details
                st.success("Reservation found!")
                st.write(f"**Name**: {record['Your Name']}")
                st.write(f"**Cat's Name**: {record['Cat\'s Name']}")
                st.write(f"**Room Type**: {record['Select Room Type']}")
                st.write(f"**Check-In Date**: {record['Check-In Date']}")
            else:
                # No matching record
                st.error("No reservation matches your given information. Please check again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
