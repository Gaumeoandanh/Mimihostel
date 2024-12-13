import streamlit as st

from services.google_sheet_service import GoogleSheetService

# Configuration and Constants
APP_TITLE = "Reservation Inquiry"

# Services
gsheet_service = GoogleSheetService()

# --- Utility Functions ---
def alert(message, type="error" or "success"):
    if type == "success":
        st.session_state.inquiry_form['alert_success'] = message
        st.session_state.inquiry_form['alert_error'] = None
    else:
        st.session_state.inquiry_form['alert_success'] = None
        st.session_state.inquiry_form['alert_error'] = message


def reset_inquiry_form():
    """Resets the inquiry form state."""
    if "inquiry_form" not in st.session_state:
        st.session_state.inquiry_form = {
            "alert_error": None,
            "alert_success": None,
            "booking_id": "",
            "name": "",
            "inquiry_submitted": False,
            "inquiry_record": None
        }

def display_booking_details(inquiry_record):
    """Displays booking details in a table format."""
    st.table({
        "Name:": inquiry_record["Your Name"],
        "Cat's Name": inquiry_record["Cat's Name"],
        "Room Type": inquiry_record["Select Room Type"],
        "Check-In Date": inquiry_record["Check-In Date"],
    })

@st.dialog('Are you sure to cancel your booking? 😿')
def confirm_cancel():
    """Handles the cancellation of a booking."""
    with st.container():
        if st.button("Cancel"):
            st.rerun()

        if st.button("Yes, cancel my booking"):
            cancel_status = gsheet_service.cancel_booking(st.session_state.inquiry_form['booking_id'])
            if cancel_status['status']:
                alert(cancel_status['message'], "success")
                st.session_state.inquiry_form['inquiry_record'] = None
            else:
                alert(cancel_status['error'], "error")
            st.rerun()  # Restarts the app state

# --- Components ---
def inquiry_booking():
    """Renders the inquiry booking form."""
    reset_inquiry_form()

    # Input form
    with st.form("inquiry-form"):
        st.session_state.inquiry_form['booking_id'] = st.text_input(
            "Booking ID (*)",
            value=st.session_state.inquiry_form.get('booking_id', '')
        )
        st.session_state.inquiry_form['name'] = st.text_input(
            "Your Name (*)",
            value=st.session_state.inquiry_form.get('name', '')
        )
        st.session_state.inquiry_form['inquiry_submitted'] = st.form_submit_button("Inquiry", use_container_width=True)

    # Display alert message from session state if present
    if st.session_state.inquiry_form['alert_success']:
        st.success(st.session_state.inquiry_form['alert_success'])

    if st.session_state.inquiry_form['alert_error']:
        st.error(st.session_state.inquiry_form['alert_error'])

    # Display booking details from session state if present
    if st.session_state.inquiry_form['inquiry_record']:
        display_booking_details(st.session_state.inquiry_form['inquiry_record'])
        st.button(
            label="Cancel",
            use_container_width=True,
            on_click=confirm_cancel,
            icon=":material/delete_history:",
        )

def process_inquiry():
    """Processes the booking inquiry."""
    if not st.session_state.inquiry_form['booking_id'] or not st.session_state.inquiry_form['name']:
        alert("Both Booking ID and Your Name are required!", "error")
        return
    else:
        # Lookup booking information
        try:
            inquiry_record = gsheet_service.find_booking(
                st.session_state.inquiry_form['booking_id'],
                st.session_state.inquiry_form['name'],
            )

            if inquiry_record:
                st.session_state.inquiry_form['inquiry_record'] = inquiry_record
                alert("Reservation found!", "success")
            else:
                st.session_state.inquiry_form['inquiry_record'] = None
                alert("No reservation matches your given information. Please check again.", "error")
        except Exception as e:
            st.session_state.inquiry_form['inquiry_record'] = None
            alert(f"An error occurred: {e}", "error")
        st.rerun()

# --- Main Page ---
def main():
    """Main entry point of the app."""
    st.title(APP_TITLE)

    # Back Button
    if st.button("Back"):
        st.switch_page("home")

    # Inquiry Booking Form
    inquiry_booking()

    # Handle Submission
    if st.session_state.inquiry_form['inquiry_submitted']:
        process_inquiry()

if __name__ == "__page__":
    main()