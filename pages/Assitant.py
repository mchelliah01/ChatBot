import os
import openai
import streamlit as st
from openai import OpenAI


st.markdown("# Page 1: Parking Assistant ❄️")
st.sidebar.markdown("# Page 1: Parking Assistant❄️")

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

assistant = client.beta.assistants.create(
  name="Parking Assistant",
  instructions="You are a chatbot for providing safe parking spots. Anlayze current police reports from the report.csv file and provide possible safe spots within sf.",
  tools=[{"type": "retrieval"}],
  model="gpt-4-turbo-preview",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)