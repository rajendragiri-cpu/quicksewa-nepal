import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page setup
st.set_page_config(page_title="Quicksewa Nepal", page_icon="🛠️")

# Google Sheet URL from your link
sheet_url = "https://docs.google.com/spreadsheets/d/1Hve4wc-kttehLAXPKugaf6RJ6C6EHQwB4BmfaBzi55w/edit?usp=sharing"

# Establish Connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Quicksewa Nepal 🇳🇵")
st.markdown("---")

menu = ["Home", "Find a Worker", "Register as Worker"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("नेपालकै भरपर्दो सेवा बजारमा स्वागत छ!")
    st.image("https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=1000")
    st.write("हामी दक्ष कामदार र सेवाग्राहीलाई एउटै प्लेटफर्ममा जोड्छौँ।")

elif choice == "Find a Worker":
    st.header("उपलब्ध कामदारहरू")
    try:
        # Sheet बाट डाटा पढ्ने
        df = conn.read(spreadsheet=sheet_url, ttl=0)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("अहिलेसम्म कोही पनि दर्ता भएको छैन।")
    except Exception as e:
        st.error("डाटा देखाउन सकिएन। कृपया पर्मिसन चेक गर्नुहोस्।")

elif choice == "Register as Worker":
    st.header("कामदार दर्ता गर्नुहोस्")
    with st.form("worker_form", clear_on_submit=True):
        name = st.text_input("पूर्ण नाम")
        skill = st.selectbox("तपाईंको सीप", ["Electrician", "Plumber", "Driver", "Cleaner", "Painter", "Carpenter"])
        phone = st.text_input("सम्पर्क नम्बर (WhatsApp/Phone)")
        
        submitted = st.form_submit_button("दर्ता गर्नुहोस्")
        
        if submitted:
            if name and phone:
                try:
                    # पहिलेको डाटा तान्ने
                    existing_data = conn.read(spreadsheet=sheet_url, ttl=0)
                    # नयाँ डाटा बनाउने
                    new_worker = pd.DataFrame([{"name": name, "skill": skill, "phone": phone}])
                    # दुवैलाई जोड्ने
                    updated_df = pd.concat([existing_data, new_worker], ignore_index=True)
                    # Sheet अपडेट गर्ने
                    conn.update(spreadsheet=sheet_url, data=updated_df)
                    
                    st.success(f"बधाई छ {name}! तपाईंको विवरण सुरक्षित भयो।")
                    st.balloons()
                except Exception as e:
                    st.error("माफ गर्नुहोला! डाटा सेभ हुन सकेन। Google Sheet मा 'Editor' पर्मिसन भएको पक्का गर्नुहोस्।")
            else:
                st.warning("कृपया नाम र सम्पर्क नम्बर अनिवार्य रूपमा भर्नुहोस्।")
