import os
from dotenv import load_dotenv

load_dotenv(".env")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE"))

print(f"QDRANT_URL: {QDRANT_URL}")
print(f"QDRANT_API_KEY: {QDRANT_API_KEY}")
print(f"COLLECTION_NAME: {COLLECTION_NAME}")
print(f"VECTOR_SIZE: {VECTOR_SIZE}")