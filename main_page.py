import streamlit as st

st.markdown("# Main Page 🚨")
st.sidebar.markdown("# Main Page 🚨")

st.write("Welcome to 🚗🅿️No Smash!🅿️🚗")
st.write("This app has been designed to work with San Francisco.")
st.write("To get started, navigate to the settings page to select your preferred language and complete the assistant setup!")

st.page_link("pages/Settings.py", label="Settings", help="Language options and assistant setup.")
st.page_link("pages/ParkingAdvice.py", label="Parking Advice", help="Get general parking advice here.")
st.page_link("pages/ReportAnalysis.py", label="Report Analysis", help="Analyzes a street within a given date range.")


#Initialize the session state
if 'source_language' not in st.session_state:
    st.session_state['source_language'] = "English"
if 'target_language' not in st.session_state:
    st.session_state['target_language'] = "English"
