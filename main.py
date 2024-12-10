import streamlit as st
def main():
    st.set_page_config(layout="centered")

    with open("assets/style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    pg = st.navigation([
        st.Page(page='pages/home.py', url_path="/", default=True, title="HomePage"),
        st.Page(page='pages/booking.py', url_path="/booking", default=False, title="Booking"),
        st.Page(page='pages/check_in.py', url_path="/check-in", default=False, title="Check-In"),
        st.Page(page='pages/chat.py', url_path="/chat", default=False, title="Chat With Me"),
    ])
    pg.run()

if __name__ == "__main__":
    main()