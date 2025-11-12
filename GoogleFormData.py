import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

@st.cache_data(ttl=30)
def load_data():
    sheet = client.open_by_key("1kYT50a_poiLoHg2gd3WzoRfN8EGs72ROHXGm7NTPXeA").sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

df = load_data()
st.dataframe(df)
