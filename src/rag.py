# wrote with assistance from Copilot. 
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import chromadb
import ollama
from sklearn.metrics.pairwise import cosine_similarity

# filepath: /src/rag.py

load_dotenv()

class RAGSystem:
    """RAG system using ChromaDB and Ollama embeddings."""
    
    def __init__(self):
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.embedding_model = os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')
        self.generation_model = os.getenv('GENERATION_MODEL', 'llama2')
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.HttpClient(
            host=os.getenv('CHROMA_HOST', 'localhost'),
            port=int(os.getenv('CHROMA_PORT', 8000))
        )
        
        # Get or create collection
        self.collection_name = os.getenv('COLLECTION_NAME', 'documents')
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        self.ollama_client = ollama.Client(host=self.ollama_host)
    
    def get_embedding(self, text):
        """Get embedding vector for text using Ollama."""
        response = self.ollama_client.embeddings(
            model=self.embedding_model,
            prompt=text
        )
        return response['embedding']
    
    def add_document(self, doc_id, text, metadata=None):
        """Add document to ChromaDB."""
        embedding = self.get_embedding(text)
        
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {}]
        )
    
    def search(self, query, top_k=3):
        """Search ChromaDB for relevant documents."""
        query_embedding = self.get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        documents = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                documents.append({
                    'text': doc,
                    'distance': results['distances'][0][i] if results['distances'] else 0,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                })
        
        return documents
    
    def answer_question(self, question, top_k=3, temperature=0.2):
        """Answer question using RAG."""
        # Step 1: Retrieve relevant documents
        retrieved_docs = self.search(question, top_k=top_k)
        
        # Step 2: Build context
        context = "\n".join([doc['text'] for doc in retrieved_docs])
        
        # Step 3: Create prompt
        prompt = f"""Answer the question based on the context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}

Answer:"""
        
        # Step 4: Generate answer
        response = self.ollama_client.generate(
            model=self.generation_model,
            prompt=prompt,
            temperature=temperature,
            num_predict=150,
            stream=False
        )
        
        return {
            'answer': response['response'],
            'sources': retrieved_docs
        }


if __name__ == "__main__":
    # Initialize RAG system
    rag = RAGSystem()
    
    # Example: Add documents
    documents = [
        ("doc1", "Python was created by Guido van Rossum in 1991."),
        ("doc2", "Python emphasizes code readability with significant indentation."),
        ("doc3", "JavaScript was created by Brendan Eich in 1995."),
    ]
    
    print("Adding documents to ChromaDB...\n")
    for doc_id, text in documents:
        rag.add_document(doc_id, text)
    
    # Test questions
    questions = [
        "Who created Python?",
        "When was JavaScript created?",
    ]
    
    print("Testing RAG System\n" + "="*50)
    for question in questions:
        print(f"\nQ: {question}")
        print("-" * 50)
        result = rag.answer_question(question)
        print(f"A: {result['answer']}")
        print("\nSources:")
        for i, source in enumerate(result['sources'], 1):
            print(f"  {i}. {source['text']}")
        print("="*50)