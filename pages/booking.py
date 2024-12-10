import streamlit as st
import re
import smtplib
from datetime import time  # Import time từ datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functions import connect_to_google_sheet

if st.button("Back"):
    st.switch_page(page='pages/home.py')

container = st.empty()

def validate(form_data):
    """Validates the booking form data.

    Args:
        form_data (dict): A dictionary containing the form data.

    Returns:
        dict: A dictionary containing error and warning messages. The dictionary has the following structure:
        {
            "error_messages": {},
            "warning_messages": {}
        }
    """

    error_messages = {
        'email': '',
        'name': '',
        'cat_name': '',
        'cat_age': '',
        'cat_breed': '',
        'checkin_date': '',
        'checkin_time': '',
        'note': ''
    }
    warning_messages = {}

    if form_data['email'] == "":
        error_messages['email'] = 'Please enter your email address'

    if form_data['name'] == "":
        error_messages['name'] = 'Please enter your name'

    if form_data['phone_number'] == "":
        error_messages['phone_number'] = 'Please enter your phone number'

    if form_data['cat_name'] == "":
        error_messages['cat_name'] = "Please enter your cat's name"

    if form_data['checkin_date'] == "":
        error_messages['checkin_date'] = "Please enter day representation"

    # Time validation
    if form_data['checkin_time'] and (form_data['checkin_time'] >= time(20, 0) or form_data['checkin_time'] < time(8, 0)):
        warning_messages['checkin_time'] = "The time you plan to arrive is out of our operating time so we will process your self-check-in. Please refer to the self-check-in guide :D"


    return {
        "error_messages": error_messages,
        "warning_messages": warning_messages,
    }

# Function to send a confirmation email
def send_email(to_email, booking_id, name, checkin_date, checkin_time):
    # Email configuration
    sender_email = "cathotelm@gmail.com"
    sender_password = "apfh nvpk hkue axoh"
    subject = "Booking Confirmation - Mimi Cat Boarding Service"
    message = f"""
    Dear {name},
    
    Thank you for booking with us. Here are your booking details:
    
    Booking ID: {booking_id}
    Check-In Date: {checkin_date}
    Check-In Time: {checkin_time}
    
    If you have any questions, feel free to contact us.
    
    Best regards,
    Cat Boarding Service Team
    """
    
    try:
        # Set up the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        
        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        st.success(f"Confirmation email sent to {to_email}!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Function to validate email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Streamlit app
st.title("Cat Boarding Service Booking Form", anchor=False)

# Input form
with st.form("booking-form"):
    email = st.text_input("Your Email (*)")
    phone = st.text_input("Your Phone Number (*)")
    # Remove spaces and non-digit characters
    phone = ''.join(filter(str.isdigit, phone))
    # Validate phone number length
    if phone and len(phone) < 10:
        st.warning("Phone number must be at least 10 digits long.")

    name = st.text_input("Your Name (*)")
    cat_name = st.text_input("Cat's Name (*)")
    cat_age = st.number_input("Cat's Age", step=0.1, min_value=0.1, format="%0.1f", value=1.0)
    cat_breed = st.text_input("Cat's Breed")
    room_type = st.selectbox("Select Room Type", ["Standard", "Deluxe", "VIP"])
    checkin_date = st.date_input("Check-In Date (*)")

    checkin_time = st.time_input("Check-In Time")
    if checkin_time and (checkin_time >= time(20, 0) or checkin_time < time(8, 0)):
        st.warning("The time you plan to arrive is out of our operating time so we will process your self-check-in. Please refer to the self-check-in guide :D")

    note = st.text_area("Note")
    # Submit button
    submitted = st.form_submit_button("Submit", use_container_width=True)

if submitted:
    if not phone.isdigit() or len(phone) < 10:
        st.error("Phone number must consist of only digits and be at least 10 digits long.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    elif email and phone and name and cat_name and checkin_date:
        try:
            # Connect to Google Sheets
            sheet = connect_to_google_sheet()

            # Generate a unique booking ID
            row_count = len(sheet.get_all_values())  # Count the current rows
            booking_id = f"BKG-{row_count + 1:04d}"  # Generate ID like "BKG-0001"

            # Prepare data
            data = [
                booking_id, email, phone, name, cat_name,
                cat_age, cat_breed, room_type,
                str(checkin_date), str(checkin_time), note
            ]

            # Append the data to the spreadsheet
            sheet.append_row(data)

            # Send confirmation email
            send_email(email, booking_id, name, checkin_date, checkin_time)

            st.success(f"Your booking has been successfully saved! Booking ID: {booking_id}")
            st.page_link(page='pages/home.py', label="Home")
        except Exception as e:
            # st.error(f"An error occurred: {e}")
            st.write(e)
    else:
        st.warning("Please fill in all required fields (*)!")
