import streamlit as st
import time
import os
import openai
from openai import OpenAI
from functions.translate import translate

openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

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
        assistant_id=assistant.id
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
    date_range = st.text_input("Enter a date, ranging from January 2018 to April 2024: ")
    st.caption("Example: January 2024 to March 2024")
    
    submitted = st.form_submit_button("Submit")

    if st.session_state['source_language'] != st.session_state['target_language']:
        st.caption(f'Translating into {st.session_state["target_language"]} from {st.session_state["source_language"]}')
    
    if submitted: # Create assistant only AFTER hitting submit?
        if st.session_state['source_language'] != st.session_state['target_language']:
            text = thread(street, date_range)
            st.write(f"Translated into {st.session_state['target_language']}")
            st.write(translate(text, st.session_state['source_language'], st.session_state['target_language']))
        else:
            st.write(thread(street, date_range))