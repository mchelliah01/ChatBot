import streamlit as st
import time
import os
import openai
from openai import OpenAI
from pages.translate import translate

openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

def thread(street, date_range):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"Street: {street} || Date range: {date_range}"
            }
        ]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_br2JCiPSMrUesGqOkFyATP58"
    )

    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(run.status)
        time.sleep(5)

    message_response = client.beta.threads.messages.list(thread.id)
    messages = message_response.data[0].content[0].text.value
    
    return messages

# Streamlit
st.markdown("# Page 2: Parking Advice 🚨")
st.sidebar.markdown("# Page 2: Parking Advice 🚨")

st.title("SFPD Incident Report Analyzer")

with st.form(key = "chat"):

    st.header("Street Name")
    street = st.text_input("Enter a street name within San Francisco: ") 
    st.caption("Example: McAllister St")

    st.header("Date Range")
    date_range = st.text_input("Enter a date, ranging from January 2018 to March 2024: ")
    st.caption("Example: January 2024 to March 2024")
    
    submitted = st.form_submit_button("Submit")

    if st.session_state['source_language'] != st.session_state['target_language']:
        st.caption(f'Translating into {st.session_state['target_language']} from {st.session_state['source_language']}')
    
    if submitted:
        if st.session_state['source_language'] != st.session_state['target_language']:
            text = thread(street, date_range)
            st.write(f'Translated into {st.session_state['target_language']}')
            st.write(translate(text, st.session_state['source_language'], st.session_state['target_language']))
        else:
            st.write(thread(street, date_range))