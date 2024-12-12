import streamlit as st
import gspread

class GoogleSheetService:
    worksheets = {}

    def __init__(self):
        # Load the service account key from the environment variable
        if not st.secrets.connections.gsheets:
            raise ValueError("Please config connections.gsheets.")

    def get_worksheet(self, worksheet_id):
        # Load from cache
        if worksheet_id in self.worksheets:
            return self.worksheets[worksheet_id]

        credentials = {
            "spreadsheet": st.secrets.connections.gsheets.spreadsheet,
            "worksheet": worksheet_id,
            "type": st.secrets.connections.gsheets.type,
            "project_id": st.secrets.connections.gsheets.project_id,
            "private_key_id": st.secrets.connections.gsheets.private_key_id,
            "private_key": st.secrets.connections.gsheets.private_key,
            "client_email": st.secrets.connections.gsheets.client_email,
            "client_id": st.secrets.connections.gsheets.client_id,
            "auth_uri": st.secrets.connections.gsheets.auth_uri,
            "token_uri": st.secrets.connections.gsheets.token_uri,
            "auth_provider_x509_cert_url": st.secrets.connections.gsheets.auth_provider_x509_cert_url,
            "client_x509_cert_url": st.secrets.connections.gsheets.client_x509_cert_url,
            "universe_domain": st.secrets.connections.gsheets.universe_domain,
        }

        # Create a Google Sheets
        client = gspread.service_account_from_dict(credentials)

        # Open the spreadsheet by URL
        sheet = client.open_by_url(st.secrets.connections.gsheets.spreadsheet)

        # Store the worksheet instance in the cache for future use
        self.worksheets[worksheet_id] = sheet.get_worksheet_by_id(worksheet_id)

        # Open the Booking sheet
        return self.worksheets[worksheet_id]

    # Find a booking by Booking ID and Name
    def find_booking(self, booking_id, name):
        try :
            # Open the Booking sheet
            worksheet = self.get_worksheet(st.secrets.connections.gsheets.worksheet)

            # Strip leading and trailing whitespace from the booking ID and name
            booking_id = booking_id.strip()
            name = name.strip()

            # Find the first cell that matches the booking ID and name
            cell = worksheet.find(booking_id)
            if cell:
                # Get the row number of the found cell
                row = cell.row

                # Get the values of the entire row
                record = worksheet.row_values(row)
                # Create a dictionary from the record
                record_dict = {header: value for header, value in zip(worksheet.row_values(1), record)}

                if record_dict['Your Name'].strip() == name and record_dict['Booking ID'].strip() == booking_id:
                    return record_dict
        except Exception as e:
            print(f"Error: {e}")

        return None  # Return None if no match is found

    def cancel_booking(self, booking_id):
        try :
            # Open the Booking sheet
            worksheet = self.get_worksheet(st.secrets.connections.gsheets.worksheet)

            # Strip leading and trailing whitespace from the booking ID and name
            booking_id = booking_id.strip()

            # Find the first cell that matches the booking ID and name
            cell = worksheet.find(booking_id)
            if cell:
                # Get the row number of the found cell
                row = cell.row

                # Get the values of the entire row
                record = worksheet.row_values(row)
                # Create a dictionary from the record
                record_dict = {header: value for header, value in zip(worksheet.row_values(1), record)}

                if record_dict['Booking ID'].strip() == booking_id:
                    return record_dict

                worksheet.delete_row(row)
        except Exception as e:
            print(f"Error: {e}")

        return None  # Return None if no match is found