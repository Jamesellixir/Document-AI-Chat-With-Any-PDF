from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def build_vector_store(chunks: list[str]) -> FAISS:
    """Embed text chunks and build an in-memory FAISS index."""
    # Convert raw strings to LangChain Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # This calls the OpenAI API once per batch of chunks
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store


def get_relevant_chunks(vector_store: FAISS, query: str, k: int = 4) -> list[str]:
    """Retrieve the k most relevant chunks for a given query."""
    results = vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]