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
    # Load environment variables
    load_dotenv()
    QDRANT_HOST = os.getenv('QDRANT_HOST')
    QDRANT_PORT = int(os.getenv('QDRANT_PORT'))
    QDRANT_COLLECTION = os.getenv('QDRANT_COLLECTION')

    # Initialize Qdrant client
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    # use cosine similarity to find the most relevant content in the vector database
    try:
        query_embedding = get_embedding(query)
    except Exception as e:
        raise ValueError(
            "Failed to generate embedding for query. Possible causes include "
            "API/connectivity issues with the embedding service, an invalid query "
            "format or type, or misconfigured environment/model settings. "
            f"Original error: {e}"
        )

    response = client.search(
        collection_name=QDRANT_COLLECTION,
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
