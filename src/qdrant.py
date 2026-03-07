from qdrant_client import QdrantClient, models
import json
from vectorEmbedding import get_embedding
from dotenv import load_dotenv
import os

# process and upload tweaked by gemini

# --- CONFIGURATION ---
load_dotenv(".env")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE"))

qdrant_client = QdrantClient(
    url=QDRANT_URL, 
    api_key=QDRANT_API_KEY,
)

def create_collection():
    try:
        qdrant_client.create_collection(    
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            ),
        )
    except Exception as e:
        print(f"Error creating collection: {e}")


def setup_collection():
    print(f"Recreating collection: {COLLECTION_NAME}")
    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE,
            distance=models.Distance.COSINE
        ),
    )

def upload_point(col_name, vector, metadata):
    qdrant_client.upsert(
        collection_name=col_name,
        points=[
            models.PointStruct(
                id=metadata['id'],
                vector=vector,
                payload=metadata
            )
        ]
    )

def process_and_upload():
    """Reads cleaned content, generates embeddings, and uploads to Qdrant."""
    with open("data/chunks/chunks.json", 'r') as f:
        data = json.load(f)

    print(f"Found {len(data)} items to process.")
    
    for i, item in enumerate(data):
        title = item.get("title", "").split('?')[-1]
        text_content = item.get("text", "")
        
        if not text_content:
            continue

        print(f"[{i+1}/{len(data)}] Generating embedding for: {title}")
        vector = get_embedding(text_content)
        
        if vector:
            meta = {'id': i, 'title': title, 'content': text_content, 'url': item.get("url")}
            upload_point(COLLECTION_NAME, vector, meta)
        else:
            print(f"Skipping {title} due to embedding error.")

if __name__ == "__main__":
    # 1. Initialize collection (Optional: comment out if you want to persist data)
    create_collection()
