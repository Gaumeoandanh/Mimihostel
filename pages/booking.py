import streamlit as st
from datetime import time  # Import time từ datetime
from functions import is_valid_email, generate_booking_id
from services.google_sheet_service import GoogleSheetService
from services.mail_service import MailService

class BookingModule:
    """
    Class for the Cat Boarding Service Booking Module.
    """

    # Services
    mail_service = MailService()
    gsheet_service = GoogleSheetService()

    # Form Data
    form_data = {
        "email": None,
        "phone": "",
        "name": None,
        "cat_name": None,
        "cat_age": None,
        "cat_breed": None,
        "room_type": None,
        "checkin_date": None,
        "checkin_time": None
    }

    # Variables
    submitted = False
    is_booked = False

    def run(self):
        self._render_ui()
        self._load_behaviours()

    def _render_ui(self):
        if st.button("Back"):
            st.switch_page(page='pages/home.py')

        # Streamlit app
        st.title("Cat Boarding Service Booking Form", anchor=False)

        # Input form
        with st.form("booking-form"):
            self.form_data['email'] = st.text_input("Your Email (*)").strip()
            self.form_data['phone'] = st.text_input("Your Phone Number (*)").strip()
            # Remove spaces and non-digit characters
            self.form_data['phone'] = ''.join(filter(str.isdigit, self.form_data['phone']))
            # Validate phone number length
            if self.form_data['phone'] and len(self.form_data['phone']) < 10:
                st.warning("Phone number must be at least 10 digits long.")

            self.form_data['name'] = st.text_input("Your Name (*)").strip()
            self.form_data['cat_name'] = st.text_input("Cat's Name (*)").strip()
            self.form_data['cat_age'] = st.number_input("Cat's Age", step=0.1, min_value=0.1, format="%0.1f", value=1.0)
            self.form_data['cat_breed'] = st.text_input("Cat's Breed").strip()
            self.form_data['room_type'] = st.selectbox("Select Room Type", ["Standard", "Deluxe", "VIP"]).strip()
            self.form_data['checkin_date'] = st.date_input("Check-In Date (*)")

            self.form_data['checkin_time'] = st.time_input("Check-In Time")
            if self.form_data['checkin_time'] and (
                self.form_data['checkin_time'] >= time(20, 0) or
                self.form_data['checkin_time'] < time(8, 0)
            ):
                st.warning("The time you plan to arrive is out of our operating time so we will process your self-check-in. Please refer to the self-check-in guide :D")

            self.form_data['note'] = st.text_area("Note").strip()
            # Submit button
            self.submitted = st.form_submit_button(
                label="Submit",
                use_container_width=True,
                disabled=self.is_booked,
            )
    def _load_behaviours(self):
        if self.submitted:
            if not is_valid_email(self.form_data['email']):
                st.error("Please enter a valid email address.")
            elif not self.form_data['phone'].isdigit() or len(self.form_data['phone']) < 10:
                st.error("Phone number must consist of only digits and be at least 10 digits long.")
            elif self.form_data['email'] and self.form_data['phone'] and self.form_data['name'] and self.form_data['cat_name'] and self.form_data['checkin_date']:
                try:
                    # Connect to Google Sheets
                    sheet = self.gsheet_service.get_worksheet(st.secrets.connections.gsheets.worksheet)

                    # Generate a unique booking ID
                    row_count = len(sheet.get_all_values())  # Count the current rows
                    booking_id = generate_booking_id(row_count)

                    # Prepare data
                    data = [
                        booking_id,
                        self.form_data['email'],
                        self.form_data['phone'],
                        self.form_data['name'],
                        self.form_data['cat_name'],
                        self.form_data['cat_age'],
                        self.form_data['cat_breed'],
                        self.form_data['room_type'],
                        str(self.form_data['checkin_date']),
                        str(self.form_data['checkin_time']),
                        self.form_data['note'],
                    ]

                    # Append the data to the spreadsheet
                    # sheet.append_row(data)

                    # Send confirmation email
                    self.mail_service.send_booking_email(
                        self.form_data['email'],
                        booking_id,
                        self.form_data['name'],
                        str(self.form_data['checkin_date']),
                        str(self.form_data['checkin_time']),
                    )

                    st.success(f"Your booking has been successfully saved! Booking ID: {booking_id}")
                    st.page_link(page='pages/home.py', label="Home")
                    self.is_booked = True
                except Exception as e:
                    # st.error(f"An error occurred: {e}")
                    st.write(e)
            else:
                st.warning("Please fill in all required fields (*)!")

booking_module = BookingModule()
booking_module.run()