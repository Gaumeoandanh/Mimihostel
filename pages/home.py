import streamlit as st

st.title("Welcome to Mimi Hotel")
# Hiển thị logo và tên
with st.container(key="logo-container"):
    st.image("assets/logo.png", width=400)

if st.button('Booking', use_container_width=True):
    st.switch_page(page='pages/booking.py')

if st.button('Check Your Mimi Reservation', use_container_width=True):
    st.switch_page(page="pages/check_in.py")

if st.button('Chat with me', use_container_width=True):
    st.switch_page(page="pages/chat.py")