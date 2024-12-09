import streamlit as st

st.title("Welcome to Mimi Hotel")
# Hiển thị logo và tên
st.markdown("""
    <div class="title">
        Am <h1>MiMi</h1> Bot
    </div>
""", unsafe_allow_html=True)
with st.container(key="logo-container"):
    st.image("cat.png", width=200)
    st.write("How may I help you!")

if st.button('Booking', use_container_width=True):
    st.switch_page(page='pages/booking.py')

if st.button('Check Your Mimi Reservation', use_container_width=True):
    st.switch_page(page="pages/check_in.py")

if st.button('Chat with me', use_container_width=True):
    st.switch_page(page="pages/chat.py")