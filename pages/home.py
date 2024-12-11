import streamlit as st

class HomePageModule:
    button_booking = None
    button_reservation = None
    button_chat = None

    def run(self):
        self._render_ui()
        self._load_behaviors()

    def _render_ui(self):
        st.title('Welcome to **MiMi** Hotel', anchor=False)

        with st.container(key="logo-container"):
            st.image("assets/logo.png", width=400)

        self.button_booking = st.button(
            label='Booking',
            use_container_width=True,
            key="button-service-booking",
        )

        self.button_reservation = st.button(
            label='Check Your Mimi Reservation',
            use_container_width=True,
            key="button-service-check-in",
        )

        self.button_chat = st.button(
            label='Chat with me',
            use_container_width=True,
            key="button-service-chat",
        )

    def _load_behaviors(self):
        if self.button_booking:
            st.switch_page(page='pages/booking.py')

        if self.button_reservation:
            st.switch_page(page='pages/reservation_inquiry.py')

        if self.button_chat:
            st.switch_page(page='pages/chat.py')

home_page_module = HomePageModule()
home_page_module.run()
