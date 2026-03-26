import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import random

# १. प्रिमियम सेटिङ र लेआउट
st.set_page_config(page_title="Quicksewa Nepal | Pathao for Services", page_icon="🛵", layout="wide")

# CSS बाट डिजाइन प्रिमियम बनाउने
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #00b894; color: white; border: none; }
    .stButton>button:hover { background-color: #009473; border: none; }
    .job-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 5px solid #00b894; }
    .price-tag { font-size: 24px; font-weight: bold; color: #2d3436; }
    </style>
    """, unsafe_allow_html=True)

# २. गुगल सिट कनेक्सन
conn = st.connection("gsheets", type=GSheetsConnection)

# साइडबार नेभिगेसन
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1063/1063376.png", width=100)
st.sidebar.title("Quicksewa Menu")
role = st.sidebar.selectbox("तपाईं को हो?", ["🏠 Home", "🧑‍प्रयोक्ता (Customer)", "👷 सेवा प्रदायक (Worker/Partner)"])

# ३. डाटा लोड गर्ने फङ्सन
def get_data():
    return conn.read(ttl=0)

# ---------------------------------------------------------
# मोड १: गृह पृष्ठ (HOME)
# ---------------------------------------------------------
if role == "🏠 Home":
    st.title("🛵 Quicksewa Nepal")
    st.subheader("महेन्द्रनगरको पहिलो डिजिटल सेवा मार्केटप्लेस")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("सक्रिय कामदार", "१५०+", "+१२ आज")
    col2.metric("पूरा भएका सेवा", "१,२००+", "९८% सफल")
    col3.metric("औसत समय", "२५ मिनेट", "-५ मिनेट")

    st.markdown("---")
    st.write("### हामीले दिने सेवाहरू:")
    st.button("🔌 इलेक्ट्रिसियन")
    st.button("🚰 प्लम्बर")
    st.button("🧹 घर सरसफाई")
    st.button("🛠️ मर्मत सम्भार")

# ---------------------------------------------------------
# मोड २: ग्राहक सेक्सन (CUSTOMER - Pathao Style)
# ---------------------------------------------------------
elif role == "🧑‍प्रयोक्ता (Customer)":
    st.header("📍 सेवा बुक गर्नुहोस्")
    
    tab1, tab2 = st.tabs(["नयाँ रिक्वेस्ट", "मेरो इतिहास"])
    
    with tab1:
        col_form, col_map = st.columns([1, 1.2])
        
        with col_form:
            with st.form("booking_form"):
                service = st.selectbox("कुन सेवा चाहियो?", ["Electrician", "Plumber", "Carpenter", "Painter", "AC Repair"])
                budget = st.number_input("तपाईंले दिन सक्ने अधिकतम रकम (Rs.)", min_value=100, value=500, step=50)
                desc = st.text_area("कामको बारेमा थप जानकारी", placeholder="जस्तै: घरको पछाडिको ट्याङ्की लिक भएको छ...")
                
                st.write("---")
                c_name = st.text_input("तपाईंको नाम")
                c_phone = st.text_input("मोबाइल नम्बर")
                
                # GPS Coordinates
                u_lat = st.number_input("अक्षांश (Lat)", value=28.9873, format="%.6f")
                u_lon = st.number_input("देशान्तर (Lon)", value=80.1652, format="%.6f")
                
                submit = st.form_submit_button("सेवा खोज्नुहोस् (Request Now)")
                
                if submit:
                    if c_name and c_phone:
                        new_data = pd.DataFrame([{
                            "ID": random.randint(1000, 9999),
                            "Role": "Request",
                            "Customer": c_name,
                            "Phone": c_phone,
                            "Service": service,
                            "Budget": budget,
                            "Detail": desc,
                            "Lat": u_lat,
                            "Lon": u_lon,
                            "Status": "Searching",
                            "Time": datetime.datetime.now().strftime("%I:%M %p")
                        }])
                        df = get_data()
                        updated = pd.concat([df, new_data], ignore_index=True)
                        conn.update(data=updated)
                        st.success("सफलतापूर्वक अनुरोध पठाइयो! कामदारहरूले बिडिङ गर्दैछन्...")
                        st.balloons()
                    else:
                        st.error("कृपया सबै विवरण भर्नुहोस्।")

        with col_map:
            st.write("**तपाईंको हालको लोकेसन:**")
            map_df = pd.DataFrame({'lat': [u_lat], 'lon': [u_lon]})
            st.map(map_df, zoom=14)
            st.info("नजिकैका कामदारहरूलाई तपाईंको लोकेसन पठाइनेछ।")

# ---------------------------------------------------------
# मोड ३: कामदार सेक्सन (WORKER - inDrive Style Bidding)
# ---------------------------------------------------------
elif role == "👷 सेवा प्रदायक (Worker/Partner)":
    st.header("💼 उपलब्ध कामहरू (Live Job Feed)")
    st.caption("रिफ्रेस गरेर नयाँ कामहरू हेर्नुहोस्")

    if st.button("कामहरू रिफ्रेस गर्नुहोस् 🔄"):
        st.rerun()

    data = get_data()
    
    if not data.empty and 'Role' in data.columns:
        pending_jobs = data[(data['Role'] == 'Request') & (data['Status'] == 'Searching')]
        
        if not pending_jobs.empty:
            for index, job in pending_jobs.iterrows():
                st.markdown(f"""
                <div class="job-card">
                    <span style="color: #00b894; font-weight: bold;">NEW REQUEST</span>
                    <h3>🛠️ {job['Service']}</h3>
                    <p><b>ग्राहक:</b> {job['Customer']} | <b>समय:</b> {job['Time']}</p>
                    <p><b>विवरण:</b> {job['Detail']}</p>
                    <div class="price-tag">प्रस्तावित बजेट: Rs. {job['Budget']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col_btn1, col_btn2, col_map_mini = st.columns([1, 1, 2])
                
                with col_btn1:
                    if st.button(f"स्वीकार गर्नुहोस् (Accept) - {job['ID']}", key=f"acc_{index}"):
                        st.success(f"तपाईंले काम पाउनुभयो! ग्राहकलाई कल गर्नुहोस्: {job['Phone']}")
                        # यहाँ स्टेटस अपडेट गर्ने लोजिक थप्न सकिन्छ
                
                with col_btn2:
                    st.button(f"काउन्टर अफर (Negotiate) - {job['ID']}", key=f"neg_{index}")

                with col_btn2:
                     # म्याप देखाउने
                     try:
                        job_loc = pd.DataFrame({'lat': [float(job['Lat'])], 'lon': [float(job['Lon'])]})
                        st.map(job_loc, zoom=13)
                     except:
                        st.write("Map Error")
        else:
            st.info("अहिले कुनै नयाँ रिक्वेस्ट छैन।")
    else:
        st.warning("सिटमा डाटा भेटिएन।")

# ४. फुटर
st.markdown("---")
st.markdown("<center>Quicksewa Nepal - Delivering Trust in Every Service</center>", unsafe_allow_html=True)
