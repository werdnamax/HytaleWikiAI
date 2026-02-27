import ollama

client = ollama.Client(host='http://ollama.cs.wallawalla.edu:11434')
_model = 'nomic-embed-text'

def get_embedding(text):
    """
    Generates a vector embedding for the given text using Ollama.
    Defaults to 'nomic-embed-text' which is a common choice for RAG.
    """
    try:
        response = client.embed(model=_model, input=text)
        return response.embeddings[0]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None


if __name__ == "__main__":
    print(get_embedding("Hello World"))
    print("Done!")