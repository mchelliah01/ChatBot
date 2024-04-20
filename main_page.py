import streamlit as st

st.markdown("# Main Page 🚨")
st.sidebar.markdown("# Main Page 🚨")

message = "Welcome to NO Smash Parking Advice!🅿️🚗  \n Please select the designated lanaguages and get parking advice."

st.write(message)

st.session_state['source_language'] = st.radio('Select Input Language', ['English', 'French', 'German', 'Chinese'])
st.session_state['target_language'] = st.radio('Select Output Language', ['English', 'French', 'German', 'Chinese'])
