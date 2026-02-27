# wrote with assistance from Copilot. 
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import ollama
from vectorEmbedding import get_embedding

# filepath: /src/rag.py

# retrieval the relevant content (using similarity search) from the vector database and use it to answer the question.

def retrieve_relevant_content(query):
    # Initialize Qdrant client
    qdrant_client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))

    # use cosine similarity to find the most relevant content in the vector database
    query_embedding = get_embedding(query)
    response = qdrant_client.search(
        collection_name=os.getenv('COLLECTION_NAME'),
        query_vector=query_embedding,
        limit=5,
        with_payload=True
    )

    return response

def generate_answer(query, relevant_content):
    # Use Ollama to generate an answer based on the query and the relevant content
    context = "\n".join([item['payload']['content'] for item in relevant_content])
    prompt = f"Answer the following question based on the provided context:\n\nContext:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
    
    response = ollama.chat(prompt)
    return response['choices'][0]['message']['content']
