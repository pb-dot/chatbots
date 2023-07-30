import streamlit as st
from streamlit_chat import message
# utils is my created py file
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv
load_dotenv()
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

st.title("AI Tutor:")

# generated is list of bot responses and past is list of  user input
# This is done to store previous conversation
#session variable is the dict having the keys as generated past messags

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Query: ", key="input") # input box 

# "message" is streamlit chat component and "messages" is used in openai model both are different
# messages=[{role:___,content:___},{role:___,content:___}] list of dict
#  contains chat history in form of list of dict

if 'messages' not in st.session_state: # when user has not given the 1st entry 
    st.session_state['messages'] = get_initial_message()# sets the role of the bot see utils.py
 
if query:# if user has written something in the Query(text box) then
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)# it is important to specify the role is user as user messages appear on right and bot messg on left in the chat
        response = get_chatgpt_response(messages)
        messages = update_chat(messages, "assistant", response)# specify the role as assistant
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        
if st.session_state['generated']: # if the bot has any generated response then

    for i in range(len(st.session_state['generated'])-1, -1, -1): # traverse the responses of bot in reverse order so the latest remain at top
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

