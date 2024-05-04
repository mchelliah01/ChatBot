import streamlit as st

st.markdown("# Main Page 🚨")
st.sidebar.markdown("# Main Page 🚨")

st.write("Welcome to 🚗🅿️No Smash!🅿️🚗")
st.write("This app has been designed to work with San Francisco.")
st.write("To get started, navigate to the settings page to select your preferred language and complete the assistant setup!")

st.page_link("pages/Assistant.py", label="Assistant", help="Analyzes a street within a given date range.")
st.page_link("pages/ParkAnalysis.py", label="Park Analysis", help="Get general parking advice here.")
st.page_link("pages/Settings.py", label="Settings", help="Language options and assistant setup.")


#Initialize the session state
if 'source_language' not in st.session_state:
    st.session_state['source_language'] = "English"
if 'target_language' not in st.session_state:
    st.session_state['target_language'] = "English"
