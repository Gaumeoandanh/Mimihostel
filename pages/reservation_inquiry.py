import streamlit as st

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

    def _load_behaviours(self):
        if self.inquiry_submitted:
            if not self.booking_id or not self.name:
                st.error("Both Booking ID and Your Name are required!")
            else:
                # Lookup booking information
                try:
                    record = self.gsheet_service.find_booking(
                        self.booking_id,
                        self.name
                    )

                    if record:
                        # Display the booking details
                        st.success("Reservation found!")
                        st.write(f"**Name**: {record['Your Name']}")
                        st.write(f"**Cat's Name**: {record['Cat\'s Name']}")
                        st.write(f"**Room Type**: {record['Select Room Type']}")
                        st.write(f"**Check-In Date**: {record['Check-In Date']}")
                    else:
                        # No matching record
                        st.error("No reservation matches your given information. Please check again.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

reservation_inquiry_module = ReservationInquiryModule()
reservation_inquiry_module.run()