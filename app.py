import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="Quicksewa Nepal", page_icon="🇳🇵")

# Google Sheet Link (तपाईंको Sheet को Link यहाँ फेर्नुहोला)
sheet_url = "https://docs.google.com/spreadsheets/d/your-id-here/edit#gid=0"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Google Sheets Connection Error")

st.title("Quicksewa Nepal 🛠️")
menu = ["Home", "Find a Worker", "Register as Worker"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("नेपालकै भरपर्दो सेवा बजारमा स्वागत छ!")
    st.write("हामी दक्ष कामदार र सेवाग्राहीलाई एउटै प्लेटफर्ममा जोड्छौँ।")

elif choice == "Find a Worker":
    st.header("उपलब्ध कामदारहरू")
    try:
        df = conn.read(spreadsheet=sheet_url)
        st.table(df)
    except:
        st.info("अहिले कुनै कामदार उपलब्ध छैनन्।")

elif choice == "Register as Worker":
    st.header("कामदार दर्ता गर्नुहोस्")
    with st.form("worker_form"):
        name = st.text_input("नाम")
        skill = st.selectbox("सीप", ["Electrician", "Plumber", "Driver", "Cleaner"])
        phone = st.text_input("सम्पर्क नम्बर")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("डाटा सेभ भयो (Google Sheet सेटअप भएपछि)।")
