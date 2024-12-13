import streamlit as st
import pandas as pd

from services.google_sheet_service import GoogleSheetService

class ReservationInquiryModule:
    """
    Class for the Reservation Inquiry Module in Mimihostel.
    """

    # Services
    gsheet_service = GoogleSheetService()

    # Variables
    booking_id = None
    name = None
    inquiry_submitted = None
    inquiry_record = None

    def run(self):
        self._render_ui()
        self._load_behaviours()

    def _render_ui(self):
        if st.button("Back"):
            st.switch_page(page='pages/home.py')

        # Streamlit app for the Inquiry Page
        st.title("Reservation Inquiry Service", anchor=False)

        # Input form
        with st.form("inquiry_form"):
            self.booking_id = st.text_input("Booking ID (*)")
            self.name = st.text_input("Your Name (*)")

            # Inquiry button
            self.inquiry_submitted = st.form_submit_button("Inquiry", use_container_width=True)
            # st.form_submit_button("Cancel", use_container_width=True, on_click=self._confirm_cancel, icon=":material/delete_history:")

        self.result = st.empty()

    def _load_behaviours(self):
        self._submit_form()

    def _submit_form(self):
         if self.inquiry_submitted:
            if not self.booking_id or not self.name:
                st.error("Both Booking ID and Your Name are required!")
                self.inquiry_record = None
            else:
                # Lookup booking information
                try:
                    self.inquiry_record = self.gsheet_service.find_booking(self.booking_id, self.name)
                    if self.inquiry_record:
                        # Display the booking details
                        st.success("Reservation found!")
                        # Display the table
                        st.table({
                            "Name:": self.inquiry_record["Your Name"],
                            "Cat's Name": self.inquiry_record["Cat's Name"],
                            "Room Type": self.inquiry_record["Select Room Type"],
                            "Check-In Date": self.inquiry_record["Check-In Date"],
                        })
                    else:
                        # No matching record
                        st.error("No reservation matches your given information. Please check again.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    @st.dialog('Are you sure to cancel your booking? 😿')
    def _confirm_cancel(self):
        if st.button("I am confirm"):
            if self.gsheet_service.cancel_booking(self.booking_id):
                st.rerun()
                st.success("Your booking has been canceled.")
            # st.rerun()

reservation_inquiry_module = ReservationInquiryModule()
reservation_inquiry_module.run()