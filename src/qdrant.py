from qdrant_client import QdrantClient, models
import json


qdrant_client = QdrantClient(
    url="https://43a3aab5-330f-4a32-b9ec-5bb8967cdad6.us-west-2-0.aws.cloud.qdrant.io", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ncm-ibH0do4IO9dbA4AveDnKwxF0Cpg1PiUbqGfVpx0",
)

print(qdrant_client.get_collections())

def get_embedding(text, model="MODEL_HERE"):
    """Isolates Ollama: just give it text, get back a list of numbers."""
    response = ollama.embeddings(model=model, prompt=text)
    return response['embedding']

with open("data/semantics/cleaned_content.json", 'r') as f:
    data = json.load(f)

def upload(client, col_name, vector, metadata):
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

def get_embeddings(text):
    

for i, item in enumerate(data):
    title = item.get("url").split('/')[-1].replace('-', ' ')

    text_content = item.get("content")
    vector = get_embeddings(text_content)
    
    meta = {'id' : i, 'title' : title, 'content' : text_content}
    upload(qdrant_client, "Hytale-Wiki-3", vector, meta)
  

qdrant_client.recreate_collection(
    collection_name="Hytale-Wiki-3",
    vectors_config=models.VectorParams(
        size=768,  # Change this to match your specific model!
        distance=models.Distance.COSINE
    ),
)


# 3. Prepare and Upload your data
# Qdrant's upload_collection is the easiest way to batch upload
qdrant_client.upload_collection(
    collection_name="Hytale-Wiki-3",
    vectors=None, # If you want Qdrant to handle embedding, or pass your list of vectors here
    payload=[{"title": name, "content": content} for name, content in zip(names, params)],
    ids=None # Automatically generates IDs if None
)