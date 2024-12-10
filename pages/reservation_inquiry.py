import streamlit as st

from functions import connect_to_google_sheet

if st.button("Back"):
    st.switch_page(page='pages/home.py')

# Function to find a booking by Booking ID and Name
def find_booking(booking_id, name):
    sheet = connect_to_google_sheet()
    records = sheet.get_all_records()  # Get all records from the sheet

    for record in records:
        if record.get("Booking ID") == booking_id and record.get("Your Name") == name:
            return record  # Return the matching record
    
    return None  # Return None if no match is found

# Streamlit app for the Inquiry Page
st.title("Reservation Inquiry Service", anchor=False)

# Input form
with st.form("inquiry_form"):
    booking_id = st.text_input("Booking ID (*)")
    name = st.text_input("Your Name (*)")

    # Inquiry button
    inquiry_submitted = st.form_submit_button("Inquiry", use_container_width=True)

if inquiry_submitted:
    if not booking_id or not name:
        st.error("Both Booking ID and Your Name are required!")
    else:
        # Lookup booking information
        try:
            record = find_booking(booking_id, name)

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
