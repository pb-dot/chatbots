### setup open_ai

import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Configure OpenAI API with the retrieved API key
openai.api_key = api_key


import streamlit as st
st.header("GPT-3 Restaurant Review Replier")
review  = st.text_area("Enter Customer Review")#creating text-box
button = st.button("Generate Reply")

def generate_reply(review):
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"This is a restaurant review replier bot. If the customer has any concerns address them.\n\nReview:{review}\n\nreplay:",
    temperature=0.7,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    #st.write(response)
    return response.choices[0].text

if button and review:# ie if user has pressed button and written something in review
    with st.spinner("Generating Reply..."):
        reply = generate_reply(review)
    st.write(reply)