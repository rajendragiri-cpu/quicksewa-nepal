import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Title
st.title("Quicksewa Nepal - Worker Registration")

# १. सिधै कनेक्सन गर्ने (केही कन्फिगर गर्नु पर्दैन)
# यसले तपाइँको Secrets मा भएको [connections.gsheets] सेक्सन सिधै तान्छ
conn = st.connection("gsheets", type=GSheetsConnection)

# २. तपाईंको Google Sheet को URL (यहाँ तपाईंको शीटको लिंक हाल्नुहोस्)
# नोट: यो लिंक कोडमै छ, त्यसैले Secrets मा हाल्नु पर्दैन
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Xy_तपाईंको_सिट_आइडी_यहाँ_हुन्छ/edit#gid=0"

# फारम (Form) को डिजाइन
with st.form("registration_form"):
    name = st.text_input("पूर्ण नाम")
    skill = st.selectbox("तपाईंको सीप", ["Electrician", "Plumber", "Painter", "Carpenter"])
    phone = st.text_input("सम्पर्क नम्बर (WhatsApp/Phone)")
    
    submit_button = st.form_submit_button(label="दर्ता गर्नुहोस्")

    if submit_button:
        if name and phone:
            try:
                # सिधै डेटा थप्ने (Append गर्ने)
                data_to_add = [name, skill, phone]
                
                # पुरानो डेटा पढ्ने
                existing_data = conn.read(spreadsheet=SHEET_URL, usecols=[0,1,2])
                
                # नयाँ डेटा सिटमा पठाउने
                conn.create(spreadsheet=SHEET_URL, data=data_to_add)
                
                st.success("डाटा सफलतापूर्वक सेभ भयो!")
            except Exception as e:
                st.error(f"त्रुटि भयो: {e}")
                st.info("कृपया पक्का गर्नुहोस् कि तपाईंले Service Account Email लाई Sheet मा 'Editor' अनुमति दिनुभएको छ।")
        else:
            st.warning("कृपया सबै विवरण भर्नुहोस्।")
