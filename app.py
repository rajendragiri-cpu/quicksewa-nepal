import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page setup
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
    st.write("हामी दक्ष कामदार र सेवाग्राहीलाई एउटै प्लेटफर्ममा जोड्छौं।")

elif choice == "Find a Worker":
    st.header("उपलब्ध कामदारहरू")
    try:
        df = conn.read(spreadsheet=sheet_url, ttl=0)
        st.dataframe(df)
    except:
        st.info("अहिले कुनै पनि कामदार दर्ता भएका छैनन्।")

elif choice == "Register as Worker":
    st.header("कामदार दर्ता गर्नुहोस्")
    with st.form("worker_form"):
        name = st.text_input("पूर्ण नाम")
        skill = st.selectbox("तपाईंको सीप", ["Electrician", "Plumber", "Driver", "Cleaner", "Painter"])
        phone = st.text_input("सम्पर्क नम्बर (WhatsApp/Phone)")
        submitted = st.form_submit_button("दर्ता गर्नुहोस्")
        
        if submitted:
            if name and phone:
                try:
                    # पहिलेको डाटा पढ्ने
                    existing_data = conn.read(spreadsheet=sheet_url, ttl=0)
                    # नयाँ डाटा बनाउने
                    new_entry = pd.DataFrame([{"name": name, "skill": skill, "phone": phone}])
                    # डाटा जोड्ने
                    updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                    # अपडेट गर्ने
                    conn.update(spreadsheet=sheet_url, data=updated_df)
                    st.success(f"बधाई छ {name}! तपाईंको विवरण सुरक्षित भयो।")
                    st.balloons()
                except Exception as e:
                    st.error("डाटा सेभ हुन सकेन। कृपया तपाईंको Google Sheet मा 'Editor' पर्मिसन भएको पक्का गर्नुहोस्।")
            else:
                st.warning("कृपया सबै विवरण भर्नुहोस्।")
