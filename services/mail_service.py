import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailService:
    # Email configuration
    sender_email = st.secrets.mailer.auth.email
    sender_password = st.secrets.mailer.auth.password

    def send(self, to_email, subject, content):
        try:
            # Set up the email
            mail = MIMEMultipart()
            mail["From"] = self.sender_email
            mail["To"] = to_email
            mail["Subject"] = subject
            mail.attach(MIMEText(content, "plain"))
            # Connect to the SMTP server and send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(mail)

            return {"status": True}
        except Exception as e:
            return {
                "status": False,
                "error": str(e)
            }

    def send_booking_email(self, to_email, booking_id, name, checkin_date, checkin_time):
        subject = "Booking Confirmation - Mimi Cat Boarding Service"
        content = f"""
                   Dear {name},

                   Thank you for booking with us. Here are your booking details:

                   Booking ID: {booking_id}
                   Check-In Date: {str(checkin_date)}
                   Check-In Time: {str(checkin_time)}

                   If you have any questions, feel free to contact us.

                   Best regards,
                   Cat Boarding Service Team
                   """
        response = self.send(to_email, subject, content)
        if response["status"]:
            st.success(f"Confirmation email sent to {to_email}!")
            return True
        else:
            st.error(f"Failed to send email: {response["error"]}")
        return False
