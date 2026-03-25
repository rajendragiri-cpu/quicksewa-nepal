import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Quicksewa Nepal", page_icon="🛠️")

# Google Sheet URL
sheet_url = "https://docs.google.com/spreadsheets/d/1Hve4wc-kttehLAXPKugaf6RJ6C6EHQwB4BmfaBzi55w/edit#gid=0"

# Connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Quicksewa Nepal 🇳🇵")
menu = ["Home", "Find a Worker", "Register as Worker"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("नेपालकै भरपर्दो सेवा बजारमा स्वागत छ!")
    st.image("https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=1000")

elif choice == "Find a Worker":
    st.header("उपलब्ध कामदारहरू")
    try:
        df = conn.read(spreadsheet=sheet_url, ttl=0) # ttl=0 ले ताजा डाटा देखाउँछ
        st.table(df)
    except:
        st.error("डाटा लोड हुन सकेन।")

elif choice == "Register as Worker":
    st.header("कामदार दर्ता गर्नुहोस्")
    with st.form("worker_form"):
        name = st.text_input("नाम")
        skill = st.selectbox("सीप", ["Electrician", "Plumber", "Driver", "Cleaner"])
        phone = st.text_input("सम्पर्क नम्बर")
        submitted = st.form_submit_button("दर्ता गर्नुहोस्")
        
        if submitted:
            if name and phone:
                try:
                    # नयाँ डाटा थप्ने प्रक्रिया
                    data = conn.read(spreadsheet=sheet_url)
                    new_entry = pd.DataFrame([{"name": name, "skill": skill, "phone": phone}])
                    updated_df = pd.concat([data, new_entry], ignore_index=True)
                    conn.update(spreadsheet=sheet_url, data=updated_df)
                    st.success(f"बधाई छ {name}! दर्ता सफल भयो।")
                    st.balloons()
                except Exception as e:
                    st.error(f"केही प्राविधिक समस्या आयो। कृपया फेरि प्रयास गर्नुहोस्।")
            else:
                st.warning("कृपया नाम र नम्बर दुवै भर्नुहोस्।")
