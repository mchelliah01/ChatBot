import streamlit as st
import time
import os
import openai
from openai import OpenAI
from functions.translate import translate
import pandas as pd
#from geopy.geocoders import Nominatim                      #Disabled; See get_coordinates()

openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

df = pd.read_csv('datasets/Street_Names_20240418.csv')

def thread(street1, street2, date_range):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"Street 1: {street1} / Street 2: {street2} || Date range: {date_range}"
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

#def get_coordinates(input_address):                                #Disabled; Assistant would constantly make mistakes and ask to try the analysis again.
    loc = Nominatim(user_agent="Geopy Library")                     #Switching models to gpt-4-turbo yielded promising results, but token usage is a factor here.
    getLoc = loc.geocode(input_address)

    address = getLoc.address
    latitude = getLoc.latitude
    longitude = getLoc.longitude
    return address, latitude, longitude

# Streamlit
st.markdown("# SFPD Incident Report Analyzer 🚨")
st.sidebar.markdown("# SFPD Incident Report Analyzer 🚨")

with st.form(key = "chat"):

    c1, c2 = st.columns([1, 1], gap="medium")

    with c1:
        st.header("Intersection")
        street1 = st.selectbox("Select a street",options=df, key="sn1")
        street2 = st.selectbox("Select a street",options=df, key="sn2")

        #if confirm_address:                                                #Disabled; See get_coordinates()
            #address, latitude, longitude = get_coordinates(input_address)   #TODO: Check if city within San Francisco
            #st.write(address)

    with c2:
        st.header("Date Range")
        date1 = st.date_input("From")
        date2 = st.date_input('To')
        date_range = (f'{date1} to {date2}')

    submitted = st.form_submit_button("Analyze")
    st.caption("Disclaimer: Assistant may exaggerate when creating an intersection-specific analysis. Citywide report is generally accurate.")

    try:
        if st.session_state['source_language'] != st.session_state['target_language']:
            st.caption(f'Translating into {st.session_state["target_language"]} from {st.session_state["source_language"]}')

        if submitted:
            #address, latitude, longitude = get_coordinates(input_address)  #Disabled; See get_coordinates()
            #st.write(f"Analyzing: {address}")                               #Disabled; See get_coordinates()
            if st.session_state['source_language'] != st.session_state['target_language']:
                text = thread(street1, street2, date_range)
                st.write(f"Translated into {st.session_state['target_language']}")
                st.write(translate(text, st.session_state['source_language'], st.session_state['target_language']))
            else:
                st.write(thread(street1, street2, date_range))
    except KeyError:
        st.error("No assistant found.")
        st.page_link("pages/Settings.py", label="🚨Setup your assistant here🚨")