import streamlit as st
from assets.style import render_css
def main():
    st.set_page_config(layout="centered")

    render_css()

    pg = st.navigation([
        st.Page(page='pages/home.py', url_path="/", default=True, title="HomePage"),
        st.Page(page='pages/booking.py', url_path="/booking", default=False, title="Booking"),
        st.Page(page='pages/check_in.py', url_path="/check-in", default=False, title="Check-In"),
        st.Page(page='pages/chat.py', url_path="/chat", default=False, title="Chat With Me"),
    ])
    pg.run()

if __name__ == "__main__":
    main()