import os
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

def get_vector_store():
    """
    Initializes and returns the ChromaDB vector store.
    """
    # Requires GOOGLE_API_KEY set in the environment
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Setup persistent ChromaDB store
    persist_directory = "./chroma_db"
    
    vector_store = Chroma(
        collection_name="research_papers",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    return vector_store

def add_papers_to_store(papers: list, vector_store: Chroma):
    """
    Converts a list of paper dictionaries into Document objects 
    and adds them into the ChromaDB vector store.
    """
    documents = []
    for paper in papers:
        # We combine the title, authors, and abstract as the main semantic content
        content = f"Title: {paper['title']}\nAuthors: {', '.join(paper['authors'])}\nAbstract: {paper['abstract']}"
        
        # Meta information tracking references later
        metadata = {
            "title": paper["title"], 
            "url": paper["url"], 
            "pdf_url": paper["pdf_url"]
        }
        
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
    
    if documents:
        vector_store.add_documents(documents)
        print(f"Added {len(documents)} papers to ChromaDB vector store.")
