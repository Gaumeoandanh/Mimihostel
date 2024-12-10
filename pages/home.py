import streamlit as st

st.title("Welcome to Mimi Hotel", anchor=False)
# Hiển thị logo và tên
st.markdown("""
    <div class="title">
        Am <div class="heading">MiMi</div> Bot
    </div>
""", unsafe_allow_html=True)
with st.container(key="logo-container"):
    st.image("assets/logo.png", width=400)

if st.button(
        label='Booking',
        use_container_width=True,
        key="button-service-booking"
):
    st.switch_page(page='pages/booking.py')

if st.button(
        label='Check Your Mimi Reservation',
        use_container_width=True,
        key="button-service-check-in"
):
    st.switch_page(page="pages/reservation_inquiry.py")

if st.button(
        label='Chat with me',
        use_container_width=True,
        key="button-service-chat"
):
    st.switch_page(page="pages/chat.py")
