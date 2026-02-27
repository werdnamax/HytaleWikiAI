from rag import retrieve_relevant_content, generate_answer
from scraper import scrape_webpage
from vectorEmbedding import get_embedding
from cleaner import genSemantics
from get_endpoints import genEnd
from qdrant import process_and_upload

def main():
    query = input("Enter your question relating to Hytale: ")
    relevant_content = retrieve_relevant_content(query)
    answer = generate_answer(query, relevant_content)
    print("Answer:", answer)
    #1
    # genEnd()

    #2
    # genSemantics()

    #3
    # process_and_upload()

if __name__ == "__main__":
    main()

