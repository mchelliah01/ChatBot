import streamlit as st
import time
from openai import OpenAI

client = OpenAI(api_key='apikey')


def thread(street, date_range):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"Street: {street} || Date range:{date_range}"
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
    
    print(messages)
    return messages

with st.form(key = "chat"):
    street = st.text_input("Enter a street name within San Francisco: ") 
    date_range = st.text_input("Enter a date, ranging from January 2018 to March 2024: ")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(thread(street, date_range))