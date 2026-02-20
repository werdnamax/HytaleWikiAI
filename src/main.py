from rag import retrieve_relevant_content, generate_answer
from scraper import scrape_webpage
from vectorEmbedding import get_embedding
from cleaner import clean_text
from get_endpoints import get_endpoints

def main():
    query = input("Enter your question relating to Hytale: ")
    relevant_content = retrieve_relevant_content(query)
    answer = generate_answer(query, relevant_content)
    print("Answer:", answer)

if __name__ == "__main__":
    main()