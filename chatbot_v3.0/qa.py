## Load environment variables from .env file
import os
from dotenv import load_dotenv
load_dotenv()


# Configure OpenAI API with the retrieved API key
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')



def create_prompt(context,query):
    header = "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    return header + context + "\n\n" + query + "\n"#context is the chunk(row in our pinecone) with highest cosine similarity with our query

def generate_answer(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop = [' END']
    )
    return (response.choices[0].text).strip()