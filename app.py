import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Quicksewa Nepal", layout="centered")

st.title("🛠️ Quicksewa Nepal")
st.subheader("कामदार दर्ता फारम")

# १. सिधै कनेक्सन गर्ने
conn = st.connection("gsheets", type=GSheetsConnection)

# २. तपाईंको Google Sheet को URL (यसलाई नफेर्नुहोला)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1vOBy3S_lC7z38n_6kCj9Y2fGqX6E0wKx2L_K1P2lP_0/edit#gid=0"

with st.form("registration_form"):
    full_name = st.text_input("पूर्ण नाम")
    skill = st.selectbox("तपाईंको सीप", ["Electrician", "Plumber", "Carpenter", "Painter", "Mason"])
    contact_no = st.text_input("सम्पर्क नम्बर (WhatsApp/Phone)")
    
    submit_button = st.form_submit_button(label="दर्ता गर्नुहोस्")

    if submit_button:
        if full_name and contact_no:
            try:
                # नयाँ डाटा तयार गर्ने
                new_data = pd.DataFrame([{
                    "पूर्ण नाम": full_name,
                    "तपाईंको सीप": skill,
                    "सम्पर्क नम्बर": contact_no
                }])
                
                # Sheet बाट पुरानो डाटा तान्ने
                existing_data = conn.read(spreadsheet=SHEET_URL)
                
                # नयाँ र पुरानो डाटा मिसाउने
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                
                # सिटमा अपडेट गर्ने
                conn.update(spreadsheet=SHEET_URL, data=updated_df)
                
                st.success("✅ बधाई छ! तपाईंको विवरण सफलतापूर्वक दर्ता भयो।")
                st.balloons()
            except Exception as e:
                st.error("डाटा सेभ हुन सकेन। कृपया तपाईंको Google Sheet मा 'Editor' पर्मिसन भएको पक्का गर्नुहोस्।")
        else:
            st.warning("कृपया सबै खाली ठाउँहरू भर्नुहोस्।")
