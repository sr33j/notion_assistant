## Embed documents and associate
import os
from dotenv import load_dotenv
import openai


load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

client = openai.OpenAI()

DOC_LEN=600
OVERLAP=100

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def get_embeddings_from_page(page_text):
   ## return a list of embeddings: [embedding, page_text]
    embeddings = []
    for i in range(0, len(page_text), DOC_LEN - OVERLAP):
        embeddings.append([get_embedding(page_text[i:i+DOC_LEN]), page_text[i:i+DOC_LEN]])
    return embeddings