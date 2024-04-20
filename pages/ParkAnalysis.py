import os
import openai
import streamlit as st
from openai import OpenAI
from functions.translate import translate
from datetime import datetime

st.markdown("# Parking Advice 💬")
st.sidebar.markdown("# Parking Advice 💬")

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Your job is to help the user find parking whether if it's safe or not in the surrounding area. Please provide the user with the best parking advice based on the street name, current time, and/or surrounding environment with in San Francisco."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

with st.form(key = "chat"):
    street_name = st.text_input("Please enter a street name within SF🌉:") 
    date = st.date_input("Please select a date📅:")
    time = st.time_input("Please select a time⏰:")
    current_time = datetime.combine(date, time)
    environment = st.text_input("Please describe the surrounding environment or/and weather🌦️:")

    submitted = st.form_submit_button("Submit")

    if submitted:
        prompt = f"Street Name: {street_name}, Current Time: {current_time}, Environment: {environment}"

        if st.session_state['source_language'] != st.session_state['target_language']:
            st.caption(f'Translating into {st.session_state["target_language"]} from {st.session_state["source_language"]}')
            text = get_completion(prompt)
            st.write(translate(text, st.session_state['source_language'], st.session_state['target_language']))
        else:
            st.write(get_completion(prompt))