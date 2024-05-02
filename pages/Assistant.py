import streamlit as st
import time
import os
import openai
from openai import OpenAI
from functions.translate import translate
import pandas as pd

openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

df = pd.read_csv('datasets/Street_Names_20240418.csv')

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
        assistant_id=st.session_state['assistant']
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
st.markdown("# SFPD Incident Report Analyzer 🚨")
st.sidebar.markdown("# SFPD Incident Report Analyzer 🚨")

with st.form(key = "chat"):
    
    c1, c2 = st.columns([1, 1], gap="medium")

    with c1:
        st.header("Street Name")
        street = st.selectbox("Select a street",options=df)

    with c2:
        st.header("Date Range")
        date1 = st.date_input("From")
        date2 = st.date_input('To')
        date_range = (f'{date1} to {date2}')
    submitted = st.form_submit_button("Submit")

    try:
        if st.session_state['source_language'] != st.session_state['target_language']:
            st.caption(f'Translating into {st.session_state["target_language"]} from {st.session_state["source_language"]}')

        if submitted:
            if st.session_state['source_language'] != st.session_state['target_language']:
                text = thread(street, date_range)
                st.write(f"Translated into {st.session_state['target_language']}")
                st.write(translate(text, st.session_state['source_language'], st.session_state['target_language']))
            else:
                st.write(thread(street, date_range))
    except KeyError:
        st.error("No assistant found.")
        st.page_link("pages/Settings.py", label="🚨Setup your assistant here🚨")