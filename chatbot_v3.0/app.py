import streamlit as st
from streamlit_chat import message
from vector_search import addData,find_match
import qa
from utils import scrape_text_from_url

st.header(" pb-dot's Web-Scrapper Q&A")
url = False
query = False
options = st.radio(
    'Choose task',
    ('Ask a question','Update the Database'))

if 'Update the Database' in options:
    url = st.text_input("Enter the url of the document")#user input
    
if 'Ask a question' in options:
    query = st.text_input("Enter your question")#user input

button = st.button("Submit")

# generated is list of bot responses and past is list of  user input
# This is done to store previous conversation
#session variable is the dict having the keys as generated past messags

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []




if button and (url or query):
    if 'Update the Database' in options:
        with st.spinner("Updating Database..."):# if select update database option
            
            corpusData = scrape_text_from_url(url)#function in utils.py(web scrapper)
            addData(corpusData,url)#function in vector_search.py
            st.success("Database Updated")

    if 'Ask a question' in options:# if select ask a question option
        with st.spinner("Searching for the answer..."):
            
            
            urls,res = find_match(query,2)# function in vector_search.py; res contains 2 matched chunks from our database
            context= "\n\n".join(res)# using \n\n as seperator same as in promts(see qa.py) ; joining the two chunks
            
            prompt = qa.create_prompt(context,query)
            answer = qa.generate_answer(prompt)

            # appending the chat history
            st.session_state.past.append(query)
            st.session_state.generated.append(answer)

            st.success("Answer: "+answer)



# display chat history
if st.session_state['generated']: # if the bot has any generated response then

    for i in range(len(st.session_state['generated'])-1, -1, -1): # traverse the responses of bot in reverse order so the latest remain at top
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

            
            


       