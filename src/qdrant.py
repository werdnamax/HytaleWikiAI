from qdrant_client import QdrantClient, models
import json
from vectorEmbedding import get_embedding

# process and upload tweaked by gemini

# --- CONFIGURATION ---
QDRANT_URL = "https://43a3aab5-330f-4a32-b9ec-5bb8967cdad6.us-west-2-0.aws.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ncm-ibH0do4IO9dbA4AveDnKwxF0Cpg1PiUbqGfVpx0"
COLLECTION_NAME = "Hytale-Wiki-3"
VECTOR_SIZE = 768

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
    with open("data/semantics/cleaned_content.json", 'r') as f:
        data = json.load(f)

    print(f"Found {len(data)} items to process.")
    
    for i, item in enumerate(data):
        title = item.get("url", "").split('/')[-1].replace('-', ' ')
        text_content = item.get("content", "")
        
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
