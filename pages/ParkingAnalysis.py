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
    
    st.header("Setup")

    c1, c2 = st.columns([1, 1], gap="medium")
    with c1:
        create_submitted = st.form_submit_button("Create assistant")
        st.caption("Creates an assistant and uploads the associated 24.6MB dataset.")
    with c2:
        cleanup_submited = st.form_submit_button("Cleanup")
        st.caption("Deletes the dataset associated with your assistant.")
    st.caption("Check assistants at: https://platform.openai.com/assistants")

    c3, c4 = st.columns([1, 1], gap="medium")

    with c3:
        st.header("Street Name")
        #street = st.text_input("Enter a street name within San Francisco: ") 
        street = st.selectbox("Select a street",options=df)

    with c4:
        st.header("Date Range")
        #date_range = st.text_input("Enter a date, ranging from January 2018 to April 2024: ")
        date1 = st.date_input("From")
        date2 = st.date_input('To')
        date_range = (f'{date1} to {date2}')
    
    submitted = st.form_submit_button("Submit")

    if st.session_state['source_language'] != st.session_state['target_language']:
        st.caption(f'Translating into {st.session_state["target_language"]} from {st.session_state["source_language"]}')

    if submitted:
        if st.session_state['source_language'] != st.session_state['target_language']:
            text = thread(street, date_range)
            st.write(f"Translated into {st.session_state['target_language']}")
            st.write(translate(text, st.session_state['source_language'], st.session_state['target_language']))
        else:
            st.write(thread(street, date_range))

    if create_submitted:
        file = client.files.create(
        file=open("datasets/SF_20240414.csv", "rb"),
        purpose='assistants'
        )

        assistant = client.beta.assistants.create(
            name="Vehicle Theft Data Analysis",
            instructions="\
            You will receive a street and date range (from January 2018 to April 2024) for analysis.\n\
            # 1. With the date range, check the number of incidents that occurred in that range and tell the user. Don't check the file if the date range is invalid. Immediately stop.\n\
            # 2. With the street name, check the intersections. Pay attention under the incident_description column for the number of incidents.\n\
            # 3. Tell the user the overall number of incidents in the city that occurred within that date range compared to the number of incidents that occurred that occurred within that date range for the given street.\n\
            Keep it text only.\n\
            Take a break before responding.",
            tools=[{"type": "code_interpreter"}],
            file_ids=[file.id],
            model="gpt-3.5-turbo",
            )

        if 'assistant_key' not in st.session_state:
            st.session_state['assistant'] = assistant.id
        if 'file_key' not in st.session_state:
            st.session_state['file'] = file.id

    #Delete files from assistant
    if cleanup_submited:
        client.beta.assistants.files.delete(
            assistant_id=st.session_state['assistant'],
            file_id=st.session_state['file']
            )