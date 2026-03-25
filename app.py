import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Quicksewa Nepal", page_icon="🇳🇵")

# Google Sheet URL
sheet_url = "https://docs.google.com/spreadsheets/d/1Hve4wc-kttehLAXPKugaf6RJ6C6EHQwB4BmfaBzi55w/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Quicksewa Nepal 🛠️")
menu = ["Home", "Find a Worker", "Register as Worker"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("नेपालकै भरपर्दो सेवा बजारमा स्वागत छ!")
    st.image("https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=1000")

elif choice == "Find a Worker":
    st.header("उपलब्ध कामदारहरू")
    try:
        # यहाँ हामी सिधै सिट पढ्छौँ
        df = conn.read(spreadsheet=sheet_url)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("अहिले कुनै कामदार उपलब्ध छैनन्।")
    except Exception as e:
        st.error(f"डाटा लोड हुन सकेन। कृपया Secrets चेक गर्नुहोस्।")

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
                    # नयाँ डाटा थप्ने
                    existing_df = conn.read(spreadsheet=sheet_url)
                    import pandas as pd
                    new_row = pd.DataFrame([{"name": name, "skill": skill, "phone": phone}])
                    updated_df = pd.concat([existing_df, new_row], ignore_index=True)
                    conn.update(spreadsheet=sheet_url, data=updated_df)
                    st.success(f"बधाई छ {name}! तपाईंको विवरण सुरक्षित भयो।")
                except:
                    st.error("डाटा सेभ गर्न सकिएन। पर्मिसन चेक गर्नुहोस्।")
            else:
                st.warning("कृपया सबै विवरण भर्नुहोस्।")
