"""
## Load environment variables from .env file
import os
from dotenv import load_dotenv
load_dotenv()


# Configure OpenAI API with the retrieved API key
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')


## connecting to database(index) named chatbot-v3 Configure pine-Cone
import pinecone      
pinecone.init(      
	api_key=os.getenv('PINECONE_API_KEY'),      
	environment=os.getenv('PINECONE_ENV')      
)      
index = pinecone.Index('chatbot-v3')# database name chatbot-v3


# setting up our embedding model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

"""
#### Web scrapper scraps data from Wikepedia website uses sentence transformer as embedding and stores in pinecone database

import requests
from bs4 import BeautifulSoup

def get_html_content(url):
    response = requests.get(url)
    return response.content

def get_plain_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script"]):#remove script tags
        script.extract()
    return soup.get_text()


def split_text_into_chunks(plain_text, max_chars=2000):#break whole doc(plain text data) retrieved from the url into chunks of max 2000 charachters
    text_chunks = []#list of chunks(string of 2000 chars)
    current_chunk = ""
    for line in plain_text.split("\n"):
        if len(current_chunk) + len(line) + 1 <= max_chars:
            current_chunk += line + " "
        else:
            text_chunks.append(current_chunk.strip())
            current_chunk = line + " "
    if current_chunk:
        text_chunks.append(current_chunk.strip())
    return text_chunks

def scrape_text_from_url(url, max_chars=2000):
    html_content = get_html_content(url)
    plain_text = get_plain_text(html_content)
    text_chunks = split_text_into_chunks(plain_text, max_chars)
    return text_chunks#list of chunks(string of 2k characters)