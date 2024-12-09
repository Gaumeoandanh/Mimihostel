import streamlit as st
import random
from functions import send_otp_email
from functions import generate_booking_number
from functions import save_booking_data
from functions import load_booking_data
from datetime import time  # Import time từ datetime

if st.button("Back"):
    st.switch_page(page='pages/home.py')

st.markdown(
    """
    <style>
    .stTextInput > div > input {
        background-color: white; /* Màu nền trắng */
        color: black; /* Màu chữ đen */
        border: 1px solid #ccc; /* Viền nhẹ */
        padding: 8px; /* Tăng kích thước padding */
        border-radius: 5px; /* Bo tròn góc */
    }
    </style>
    """,
    ## mé viết vầy mà code hông chạy T.T
    unsafe_allow_html=True
)
container = st.empty()
def booking():
    with container.container():
        st.title("Booking Service")
        email = st.text_input("Your Email")
        contact = st.text_input("Your Phone Number")
        name = st.text_input("Your Name")
        cat_name = st.text_input("Cat's Name")
        cat_age = st.number_input("Cat's Age", step=0.1, min_value=0.1, format="%0.1f")
        cat_breed = st.text_input("Cat's Breed")
         # Add room type selection
        room_types = ["Standard", "Deluxe", "VIP"]
        room_type = st.selectbox("Select Room Type", options=room_types)
        date = st.date_input("Date")
        
        # Define the time input field
        time_input = st.time_input("Time (optional)")

        # Time validation
        if time_input and (time_input >= time(20, 0) or time_input < time(8, 0)):
            st.warning("The time you plan to arrive is out of our operating time so we will process your self-check-in. Please refer to the self-check-in guide :D")

        note = st.text_area("Note (optional)")

        submit = st.button("Submit", use_container_width=True)

    if submit:
        otp = ''.join(random.choices('0123456789', k=6))
        # send_otp_email(email, otp)

        booking_number = generate_booking_number()
        booking_data = {
            "booking_number": booking_number,
            "contact": phone_number,
            "email": email,
            "name": name,
            "cat_name": cat_name,
            "cat_age": cat_age,
            "cat_breed": cat_breed,
            "room_type": room_type,
            "date": str(date),
            "time": str(time),
            "note": note,
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

booking_number = st.query_params.get('booking-number')
if booking_number:
    booking_confirm(booking_number)
else:
    booking()