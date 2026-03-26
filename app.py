import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# एपको सेटिङ (Premium Look)
st.set_page_config(page_title="Quicksewa Nepal Pro", page_icon="🛠️", layout="wide")

# गुगल सिटसँग कनेक्सन
conn = st.connection("gsheets", type=GSheetsConnection)

# साइडबार मेनु (Navigation)
st.sidebar.title("🛠️ Quicksewa Nepal")
st.sidebar.markdown("---")
app_mode = st.sidebar.radio("आफ्नो रोल छान्नुहोस्:", ["🏠 गृह पृष्ठ (Home)", "🧑‍🔧 ग्राहक (Customer Request)", "👷 कामदार (Worker View)"])

# ---------------------------------------------------------
# १. गृह पृष्ठ (Home)
# ---------------------------------------------------------
if app_mode == "🏠 गृह पृष्ठ (Home)":
    st.title("Quicksewa Nepal मा स्वागत छ!")
    st.subheader("तपाईंको सेवा, हाम्रो प्रतिबद्धता")
    st.write("यहाँ तपाईंले घरमै बसेर प्लम्बर, इलेक्ट्रिसियन, र अन्य कामदार बोलाउन सक्नुहुन्छ वा कामदारको रूपमा दर्ता भएर काम पाउन सक्नुहुन्छ।")
    st.info("👈 कृपया काम सुरु गर्न देब्रेपट्टिको मेनुबाट 'ग्राहक' वा 'कामदार' छान्नुहोस्।")

# ---------------------------------------------------------
# २. ग्राहक भ्यू (Customer Request)
# ---------------------------------------------------------
elif app_mode == "🧑‍🔧 ग्राहक (Customer Request)":
    st.header("नयाँ कामको लागि अनुरोध गर्नुहोस्")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("customer_request"):
            c_name = st.text_input("तपाईंको नाम")
            c_phone = st.text_input("सम्पर्क नम्बर")
            service_needed = st.selectbox("के काम चाहिएको हो?", ["Electrician", "Plumber", "Carpenter", "Painter"])
            details = st.text_area("कामको विवरण (छोटकरीमा)")
            
            # Map Coordinates (Default: Mahendranagar/Kanchanpur area)
            st.markdown("**तपाईंको लोकेसन (Map):**")
            lat = st.number_input("Latitude (अक्षांश)", value=28.9873, format="%.6f")
            lon = st.number_input("Longitude (देशान्तर)", value=80.1652, format="%.6f")
            
            submit_request = st.form_submit_button("कामदार खोज्नुहोस् 🔍")

            if submit_request:
                if c_name and c_phone:
                    try:
                        # पुरानो डाटा तान्ने
                        existing_data = conn.read(ttl=0)
                        
                        # नयाँ डाटा बनाउने
                        new_req = pd.DataFrame([{
                            "Role": "Customer",
                            "Name": c_name,
                            "Phone": c_phone,
                            "Service": service_needed,
                            "Details": details,
                            "Status": "Pending",
                            "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Lat": lat,
                            "Lon": lon
                        }])
                        
                        # डाटा जोड्ने र अपडेट गर्ने
                        if existing_data.empty:
                            updated_data = new_req
                        else:
                            updated_data = pd.concat([existing_data, new_req], ignore_index=True)
                            
                        conn.update(data=updated_data)
                        st.success("✅ तपाईंको अनुरोध दर्ता भयो! छिट्टै नजिकैको कामदारले सम्पर्क गर्नेछन्।")
                        st.balloons()
                    except Exception as e:
                        st.error(f"त्रुटि भयो: {e}")
                else:
                    st.warning("कृपया नाम र फोन नम्बर भर्नुहोस्।")

    with col2:
        st.write("तपाईंको लोकेसन म्यापमा:")
        # म्याप देखाउने
        map_data = pd.DataFrame({'lat': [28.9873], 'lon': [80.1652]})
        st.map(map_data, zoom=12)

# ---------------------------------------------------------
# ३. कामदार भ्यू (Worker View)
# ---------------------------------------------------------
elif app_mode == "👷 कामदार (Worker View)":
    st.header("तपाईंको नजिकैका कामहरू (Live Requests)")
    
    # Refresh button to fetch new data
    if st.button("नयाँ कामहरू रिफ्रेस गर्नुहोस् 🔄"):
        st.rerun()
        
    try:
        data = conn.read(ttl=0)
        
        # Check if data exists and has the 'Role' column
        if not data.empty and 'Role' in data.columns:
            # Filter only Customer requests that are Pending
            requests = data[(data['Role'] == 'Customer') & (data['Status'] == 'Pending')]
            
            if not requests.empty:
                for index, row in requests.iterrows():
                    with st.container(border=True):
                        st.subheader(f"🛠️ {row['Service']} चाहिएको छ")
                        st.write(f"**ग्राहकको नाम:** {row['Name']} | **सम्पर्क:** {row['Phone']}")
                        st.write(f"**कामको विवरण:** {row['Details']}")
                        st.caption(f"🕒 अनुरोध गरिएको समय: {row['Time']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"काम स्वीकार गर्नुहोस् ✅", key=f"btn_{index}"):
                                st.success(f"तपाईंले {row['Name']} को काम स्वीकार गर्नुभयो! कृपया उहाँलाई {row['Phone']} मा कल गर्नुहोस्।")
                        with col2:
                            # Show specific map for this request
                            try:
                                req_map = pd.DataFrame({'lat': [float(row['Lat'])], 'lon': [float(row['Lon'])]})
                                st.map(req_map, zoom=14)
                            except:
                                st.write("लोकेसन उपलब्ध छैन")
            else:
                st.info("अहिले कुनै नयाँ काम उपलब्ध छैन। एकछिन पछि फेरि रिफ्रेस गरेर हेर्नुहोला।")
        else:
            st.info("अहिले कुनै पनि ग्राहकले कामको अनुरोध गरेका छैनन्।")
    except Exception as e:
        st.error(f"डाटा लोड हुन सकेन: {e}")
