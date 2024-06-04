import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch        
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("OPENSEARCH_SERVICE_URI")
INDEX_NAME = os.getenv("INDEX_NAME")
# Create an index

def similarity_search(query: str) -> dict:
    embeddings = HuggingFaceEmbeddings()
    vector_search = OpenSearchVectorSearch(
        index_name=INDEX_NAME,
        embedding_function=embeddings,
        opensearch_url=CONNECTION_STRING,
    )

    return vector_search.similarity_search_with_score(
        query,
        vector_field="content_vector",
        text_field="content",
        metadata_field="*",
        k=6,
    )