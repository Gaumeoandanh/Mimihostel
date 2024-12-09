import streamlit as st
from streamlit_gsheets import GSheetsConnection

class Datasource:
    instance: None
    conn: None

    def get_instance(self):
        if Datasource.instance is None:
            Datasource.instance = Datasource()
            Datasource.conn = st.connection("gsheets", type=GSheetsConnection)
        return Datasource.instance

    def test(self):
        df = self.conn.query('select * from "bookings"')

    def get_data(self, sheet):
        # Read data from the Google Sheet.
        data = self.conn.read(
            worksheet=sheet,
            ttl="1m",
        )