import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

# Initialize ChromaDB persistent client
CHROMA_PATH = "./chroma_db_data"
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Use Chroma's default sentence-transformer embedding function 
# (keeps dependencies minimal & doesn't require API keys)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Create or get the collection
collection = client.get_or_create_collection(
    name="research_papers",
    embedding_function=embedding_fn
)

def add_documents(papers: List[Dict[str, Any]]) -> None:
    """
    Store research paper abstracts into the ChromaDB vector database.
    
    Args:
        papers: List of dictionaries. Each dict should contain:
                'title' (str), 'abstract' (str), and 'metadata' (dict).
    """
    if not papers:
        print("No papers provided to add_documents.")
        return

    documents = []
    metadatas = []
    ids = []

    for i, paper in enumerate(papers):
        # We embed the abstract as the main searchable content
        documents.append(paper["abstract"])
        
        # Combine title into metadata for retrieval
        meta = paper.get("metadata", {})
        meta["title"] = paper["title"]
        metadatas.append(meta)
        
        # Generate a simple unique ID for each document
        # Using enumerate index and title snippet for uniqueness in this hackathon context
        safe_title = "".join(c for c in paper["title"] if c.isalnum()).strip()
        doc_id = f"doc_{safe_title[:15]}_{i}"
        ids.append(doc_id)

    try:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added {len(papers)} papers to 'research_papers' collection.")
    except Exception as e:
        print(f"Error adding documents to ChromaDB: {e}")

def search_documents(query: str, n_results: int = 3) -> Dict[str, Any]:
    """
    Search the vector database for the most relevant papers based on the query.
    
    Args:
        query: The search term or question.
        n_results: Max number of relevant papers to return. Default is 3.
        
    Returns:
        Dictionary containing matched documents, metadatas, and distances.
    """
    if not query:
        return {}

    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    except Exception as e:
        print(f"Error searching ChromaDB: {e}")
        return {}


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Define sample data
    sample_papers = [
        {
            "title": "Attention Is All You Need",
            "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
            "metadata": {
                "authors": "Vaswani et al.", 
                "pdf_link": "https://arxiv.org/abs/1706.03762"
            }
        },
        {
            "title": "Generative Agents: Interactive Simulacra of Human Behavior",
            "abstract": "Believable proxies of human behavior can empower interactive applications ranging from immersive environments to rehearsal spaces for interpersonal communication to prototyping tools. In this paper, we introduce generative agents--computational software agents that simulate believable human behavior.",
            "metadata": {
                "authors": "Park et al.", 
                "pdf_link": "https://arxiv.org/abs/2304.03442"
            }
        }
    ]
    
    # 2. Add documents to DB
    print("--- Adding Documents ---")
    add_documents(sample_papers)
    
    # 3. Search for relevance
    test_query = "AI systems simulating believable humans"
    print(f"\n--- Searching for: '{test_query}' ---")
    
    search_results = search_documents(test_query, n_results=1)
    
    # 4. Display results cleanly
    if search_results and search_results.get('documents') and search_results['documents'][0]:
        top_meta = search_results['metadatas'][0][0]
        top_doc = search_results['documents'][0][0]
        distance = search_results['distances'][0][0]
        
        print("\nTop Result Found:")
        print(f"Title: {top_meta.get('title')}")
        print(f"Authors: {top_meta.get('authors')}")
        print(f"Distance Score: {distance:.4f} (Lower = more relevant)")
        print(f"Abstract Snippet: {top_doc[:150]}...")
    else:
        print("No exact matches found.")
