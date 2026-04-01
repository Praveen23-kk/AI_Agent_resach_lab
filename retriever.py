from vector_store import search_documents

def retrieve_context(query: str, top_k: int = 5) -> str:
    """
    Retrieves the top N most relevant research chunks (abstracts) for a given query
    and formats them into a single context string to be fed to an LLM.
    
    Args:
        query: The user's question or search topic
        top_k: Number of relevant papers to retrieve (default: 5)
        
    Returns:
        A formatted string containing the top relevant abstracts, titles, and links,
        ready to be used as context in a RAG prompt.
    """
    # 1/2/3. Query conversion and DB Search handled by vector_store
    results = search_documents(query, n_results=top_k)
    
    # 4. Return context for the LLM
    if not results or not results.get('documents') or not results['documents'][0]:
        return "No relevant context found in the vector database."
        
    context_chunks = []
    
    # Extract the matched arrays (ChromaDB returns list of lists)
    docs = results['documents'][0]
    metas = results['metadatas'][0]
    
    # Format the retrieved papers into digestible chunks
    for doc, meta in zip(docs, metas):
        title = meta.get('title', 'Unknown Title')
        authors = meta.get('authors', 'Unknown Authors')
        pdf = meta.get('pdf_link', 'No PDF Link')
        
        chunk = (
            f"--- Paper ---\n"
            f"Title: {title}\n"
            f"Authors: {authors}\n"
            f"Link: {pdf}\n"
            f"Abstract: {doc}\n"
        )
        context_chunks.append(chunk)
        
    # Join all chunks together separated by newlines
    full_context = "\n".join(context_chunks)
    return full_context

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    test_query = "AI systems simulating believable humans"
    print(f"Retrieving context for query: '{test_query}'...\n")
    
    # Assuming 'vector_store.py' has already been run and populated the DB
    context_str = retrieve_context(test_query, top_k=2)
    
    print("--- Retrieved Context ready for LLM Delivery ---")
    print(context_str)
