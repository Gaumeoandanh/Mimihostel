import streamlit as st
import random
from functions import load_booking_data, save_booking_data

if st.button("Back"):
    st.switch_page(page='pages/home.py')

st.title("Check-In Service")

booking_number = st.text_input("Booking Number")
otp_input = st.text_input("Enter OTP")

if st.button("Get OTP", use_container_width=True):
    bookings = load_booking_data()
    booking = next((b for b in bookings if b['booking_number'] == booking_number), None)

    if booking:
        otp = ''.join(random.choices('0123456789', k=6))
        booking['otp'] = otp
        save_booking_data(bookings)

        st.success(f"OTP sent! Your new OTP is {otp}")
    else:
        st.error("Invalid booking number")

if st.button("Check", use_container_width=True):
    bookings = load_booking_data()
    booking = next((b for b in bookings if b['booking_number'] == booking_number), None)
    st.write(booking)
    if booking:
        if booking['otp'] == otp_input:
            if booking['status'] == "confirmed":
                # Display cat's status
                st.success("Check-in successful!")
                # Add code to display cat's status
            else:
                st.error("Booking is not confirmed")
        else:
            st.error("Invalid OTP")
    else:
        st.error("Invalid booking number")