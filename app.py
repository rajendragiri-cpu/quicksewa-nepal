import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Quicksewa Nepal", layout="centered")
st.title("🛠️ Quicksewa Nepal")
st.subheader("कामदार दर्ता फारम")

# 1. Connection setup
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("registration_form"):
    full_name = st.text_input("पूर्ण नाम")
    skill = st.selectbox("तपाईंको सीप", ["Electrician", "Plumber", "Carpenter", "Painter", "Mason"])
    contact_no = st.text_input("सम्पर्क नम्बर (WhatsApp/Phone)")
    
    submit_button = st.form_submit_button(label="दर्ता गर्नुहोस्")

    if submit_button:
        if full_name and contact_no:
            try:
                # 2. Sheet bata bhayeko sabai data read garne
                # ttl=0 rakhnu parcha natra purano data cache ma bascha
                existing_data = conn.read(ttl=0)
                
                # 3. Naya data ko dataframe banaune
                new_row = pd.DataFrame([{
                    "पूर्ण नाम": full_name,
                    "तपाईंको सीप": skill,
                    "सम्पर्क नम्बर": contact_no
                }])
                
                # 4. Purano ra naya data lai jodne (Concatenate)
                # Purano data khali cha bhane naya matra rakhne
                if existing_data.empty:
                    updated_df = new_row
                else:
                    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                # 5. Full updated dataframe lai Sheet ma write garne
                conn.update(data=updated_df)
                
                st.success(f"✅ {full_name} को विवरण सफलतापूर्वक दर्ता भयो!")
                st.balloons()
            except Exception as e:
                st.error(f"डाटा सेभ हुन सकेन: {e}")
        else:
            st.warning("कृपया सबै विवरण भर्नुहोस्।")
