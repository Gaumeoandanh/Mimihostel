import streamlit as st
import random
from datetime import time  # Import time từ datetime
from functions import send_otp_email
from functions import generate_booking_number
from functions import save_booking_data
from functions import load_booking_data

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

def booking():
    with container.container():
        st.title("Booking Service")
        form_data = {
            'email': st.text_input("Your Email (*)"),
            'error_email': st.empty(),

            'phone_number': st.text_input("Your Phone Number (*)"),
            'error_phone_number': st.empty(),

            'name': st.text_input("Your Name (*)"),
            'error_name': st.empty(),

            'cat_name': st.text_input("Cat's Name (*)"),
            'error_cat_name': st.empty(),

            'cat_age': st.number_input("Cat's Age", step=0.1, min_value=0.1, format="%0.1f", value=1.0),
            'cat_breed': st.text_input("Cat's Breed"),

         	# Add room type selection
	        'room_type': st.selectbox("Select Room Type", options=["Standard", "Deluxe", "VIP"]),

            'checkin_date': st.date_input("Check-In Date  (*)"),
            'error_checkin_date': st.empty(),

        	# Define the time input field
            'checkin_time': st.time_input("Check-In Time"),
            'warning_checkin_time': st.empty(),

            'note': st.text_area("Note")
        }

        validation = validate(form_data)
        submit = st.button("Submit", use_container_width=True)

    if submit:
        # Validation
        for field, warning in validation['warning_messages'].items():
            if warning != "":
                form_data[f"warning_{field}"].warning(warning)

        valid = all(value == "" for value in validation['error_messages'].values())
        if not valid:
            for field, error in validation['error_messages'].items():
                if error != "":
                    form_data[f"error_{field}"].error(error)
            st.stop()

        otp = ''.join(random.choices('0123456789', k=6))
        # send_otp_email(email, otp)

        booking_number = generate_booking_number()
        booking_data = {
            "booking_number": booking_number,
            "phone_number": form_data['phone_number'],
            "email": form_data['email'],
            "name": form_data['name'],
            "cat_name": form_data['cat_name'],
            "cat_age": form_data['cat_age'],
            "cat_breed": form_data['cat_breed'],
            "room_type": form_data['room_type'],
            "checkin_date": str(form_data['checkin_date']),
            "checkin_time": str(form_data['checkin_time']),
            "note": form_data['note'],
            "otp": otp,
            "status": "pending"
        }

        bookings = load_booking_data()
        bookings.append(booking_data)
        save_booking_data(bookings)

        st.success(f"Your booking number is {booking_number}. Please check your email for the OTP {otp}")
        st.query_params.from_dict({"booking-number": booking_number})
        container.empty()
        booking_confirm(booking_number)

def booking_confirm(booking_number):
    bookings = load_booking_data()
    booking = next((b for b in bookings if b['booking_number'] == booking_number), None)

    with container.container():
        if booking:
            st.title("Booking Confirmation")

            with st.form('booking-confirm', border=False):
                otp_input = st.text_input("Enter OTP")
                submitted = st.form_submit_button("Confirm", use_container_width=True)
                if submitted and otp_input:
                    if otp_input == booking['otp']:
                        booking['status'] = "confirmed"
                        save_booking_data(bookings)
                        container.empty()

                        with container.container():
                            st.title("Booking Confirmation")
                            st.success("Booking confirmed!")
                            st.page_link(page='pages/home.py', label="Home")
                    else:
                        st.error("Invalid OTP")

        else:
            st.error("Invalid booking number")

booking_number = st.query_params.get('booking-number', None)
if booking_number:
    booking_confirm(booking_number)
else:
    booking()