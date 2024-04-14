import streamlit as st

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

message = "Welcome to the main page! 🎉\nPlease navigate the pages to explore some sample code."

st.write(message)

source_language = st.radio('Select Source language', ['English', 'French', 'German', 'Chinese'])
target_language = st.radio('Select Target language', ['English', 'French', 'German', 'Chinese'])

###Session State###
if 'source_language_key' not in st.session_state:
    st.session_state['source_language'] = source_language
if 'target_language_key' not in st.session_state:
    st.session_state['target_language'] = target_language