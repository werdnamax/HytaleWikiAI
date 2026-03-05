import ollama
import os
from vectorEmbedding import get_embedding
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
import re

load_dotenv(".env")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY_READONLY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE"))

_client = ollama.Client(host='http://ollama.cs.wallawalla.edu:11434')
_user_prompt = "What are the different types of weapons in hytale?"

_qdrant_client = QdrantClient(
    url=QDRANT_URL, 
    api_key=QDRANT_API_KEY,
)

def get_topK(prompt, k):
    emb_prompt = get_embedding(prompt)
    response = _qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=emb_prompt,
        limit=k,
    )
    # return "\n".join([str(p.payload.get('text', '')) for p in response.points])
    return response
    
def rag(user_prompt, model='deepseek-r1:latest', top_k=3, temp=1.0):
    model_prompt = f"""You are a helpful assistant. Answer the question using ONLY the context provided below. 
        If the answer isn't in the context, say you don't know.

        Context: {get_topK(user_prompt, top_k)}

        Question: {user_prompt}

        Answer:"
    """

    response = _client.chat(
        model=model,
        options={"temperature": temp},
        messages=[{"role": "user", "content": model_prompt}]
    )

    full_content = response.message.content

    clean_answer = re.sub(r'<think>.*?</think>', '', full_content, flags=re.DOTALL).strip()

    return clean_answer

print(rag(_user_prompt, top_k=5))