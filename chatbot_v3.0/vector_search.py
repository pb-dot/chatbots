## Load environment variables from .env file
import os
from dotenv import load_dotenv
load_dotenv()

## connecting to database(index) named chatbot-v3 Configure pine-Cone
import pinecone      
pinecone.init(      
	api_key=os.getenv('PINECONE_API_KEY'),      
	environment=os.getenv('PINECONE_ENV')      
)      
index = pinecone.Index('chatbot-v3')# database name chatbot-v3

# setting up our embedding model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')#384 dimensional embedding
#model takes any length string as input and converts it into 384 dim vector

# data stored in Pinecone as
# Each row is a tuple( id=row_no. , embedding , metadata)



#the below function inserts data(chunks) as embeddngs to our databse
def addData(corpusData,url):# corpusData is the list of chunks(string of 2000 characters) we get after scrapping the url
    id = index.describe_index_stats()['total_vector_count']#total number of vectors in our DataBa
    for i in range(len(corpusData)):#iter over total no. of chunks in list of chunks
        chunk=corpusData[i]
        chunkInfo=(str(id+i),#this is the row_no
                model.encode(chunk).tolist(),#this is the embedding
                {'title': url,'context': chunk})#this is the metadata 
        index.upsert(vectors=[chunkInfo])#insert to DataBase

# as each chunk is stored as vector of 384 dim as each row in our Database
# the below function takes our Query converts it into vector and searches our database 
# ie matches 2 vectors(chunk/row,query) cosine similarity and returns top K rows/chunks

def find_match(query,k):
    query_em = model.encode(query).tolist()#embedding our Query
    result = index.query(query_em, top_k=k, includeMetadata=True)
    # note we are storing the actual chunks as metadata for its embeddings
    # returns a tuple of list with matched results metadata(dict) of title(key) and context(key) 
    # the title has the url stored and the context has the actual chunk stored
    return [result['matches'][i]['metadata']['title'] for i in range(k)],[result['matches'][i]['metadata']['context'] for i in range(k)]

# now on getting the chunk which is most related to our query we will use openai to search the chunk for the apt ans ie we will give the chunk as context to our openai model