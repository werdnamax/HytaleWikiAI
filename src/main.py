from get_endpoints import genEnd
from cleaner import genSemantics
from qdrant import process_and_upload
from chunker import genChunks
from rag import rag


def main():
    query = input("Enter a query about Hytale: ")
    print("Processing query... This may take a moment.")
    print(rag(query, top_k=5))


if __name__ == "__main__":
    main()
#1
# genEnd()

#2
# genSemantics()

#3
# genChunks()

#4
# process_and_upload()