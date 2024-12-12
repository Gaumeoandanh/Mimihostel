import streamlit as st

def main():
    st.set_page_config(layout="centered")
    with open("assets/style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    with st.container(key='banner-top-left'):
        st.image('assets/perfect.png', width=160)

    pg = st.navigation([
        st.Page(
            page='pages/home.py',
            url_path="/",
            default=True,
            title="HomePage"
        ),
        st.Page(
            page='pages/booking.py',
            url_path="/booking",
            default=False,
            title="Booking"
        ),
        st.Page(
            page='pages/reservation_inquiry.py',
            url_path="/reservation_inquiry",
            default=False,
            title="Reservation Inquiry"
        ),
        st.Page(
            page='pages/chat.py',
            url_path="/chat",
            default=False,
            title="Chat With Me"
        ),
    ])
    pg.run()

if __name__ == "__main__":
    main()