import os
import openai
import streamlit as st
from openai import OpenAI

st.markdown("# Page 2: Parking Advice ❄️")
st.sidebar.markdown("# Page 2: Parking Advice❄️")

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()
# create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Your job is to help the user find parking in the surrounding area. Please provide the user with the best parking advice."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

# create our streamlit app
with st.form(key = "chat"):
    prompt = st.text_input("Explain surrounding envrionments you would like me to explain: ") 
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(get_completion(prompt))