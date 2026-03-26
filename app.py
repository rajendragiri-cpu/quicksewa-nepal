import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Quicksewa Nepal", layout="centered")
st.title("🛠️ Quicksewa Nepal")
st.subheader("कामदार दर्ता फारम")

# १. कनेक्सन सेटअप
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("registration_form"):
    full_name = st.text_input("पूर्ण नाम")
    skill = st.selectbox("तपाईंको सीप", ["Electrician", "Plumber", "Carpenter", "Painter", "Mason"])
    contact_no = st.text_input("सम्पर्क नम्बर (WhatsApp/Phone)")
    
    submit_button = st.form_submit_button(label="दर्ता गर्नुहोस्")

    if submit_button:
        if full_name and contact_no:
            try:
                # नयाँ डाटा बनाउने
                new_row = pd.DataFrame([{
                    "पूर्ण नाम": full_name,
                    "तपाईंको सीप": skill,
                    "सम्पर्क नम्बर": contact_no
                }])
                
                # २. पुरानो डाटा पढ्ने र नयाँ थप्ने
                existing_data = conn.read()
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                # ३. सिटमा अपडेट गर्ने
                conn.update(data=updated_df)
                
                st.success("✅ सफलतापूर्वक दर्ता भयो!")
                st.balloons()
            except Exception as e:
                st.error("डाटा सेभ हुन सकेन।")
        else:
            st.warning("कृपया सबै विवरण भर्नुहोस्।")
