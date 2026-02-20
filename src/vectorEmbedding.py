## use ollama to create vector embeddings and store them in qdrant.
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import ollama


def create_embeddings(text):
  # Use Ollama to create vector embeddings for the given text
  response = ollama.embed(text)
  return response['embedding']

def store_embeddings_in_qdrant(embeddings, metadata):
  # Initialize Qdrant client
  qdrant_client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
  
  # Store embeddings in Qdrant with associated metadata
  for embedding, meta in zip(embeddings, metadata):
      qdrant_client.upsert(collection_name='hytale_wiki', points=[{
          'id': meta['id'],
          'vector': embedding,
          'payload': meta
      }])