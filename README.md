# Agentic Research Lab

An AI research assistant that takes a research question, searches academic papers via the ArXiv API, stores them in a ChromaDB vector database, and generates insights using Gemini RAG with LangChain.

## Folder Structure

```
├── .env.example               # Template for environment variables
├── README.md                  # Project overview and instructions
├── requirements.txt           # Python dependencies
├── app.py                     # Streamlit frontend application
└── src/                       # Application source code
    ├── __init__.py            
    ├── arxiv_retriever.py     # Logic for searching and fetching papers from ArXiv API
    ├── vector_store.py        # Logic for ChromaDB initialization and document ingestion
    └── rag_engine.py          # LangChain setup with Gemini and ChromaDB for Q&A
```

## File Descriptions

*   **`app.py`**: The Streamlit frontend. Provides the UI for entering search queries, fetching and indexing papers, and asking domain-specific insight questions through a conversational RAG interface.
*   **`src/arxiv_retriever.py`**: Integrates with the ArXiv API using the `arxiv` python package. Searches for relevant papers and formats the metadata and abstracts.
*   **`src/vector_store.py`**: Manages the ChromaDB instance. Initializes a persistent ChromaDB vector store and handles inserting `Document` representations of the fetched papers using Gemini Embeddings.
*   **`src/rag_engine.py`**: The core AI logic. Constructs the LangChain retrieval chain containing the Gemini LLM and the ChromaDB retriever to process user queries and generate formulated insights based on context.

## Setup Instructions

1.  **Clone / Navigate** to the project repository.
2.  **Create a Virtual Environment** (Optional but recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate # On Unix/MacOS
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Environment Variables**:
    *   Rename `.env.example` to `.env`.
    *   Add your `GOOGLE_API_KEY` to the `.env` file for Gemini access.
5.  **Run the Streamlit App**:
    ```bash
    streamlit run app.py
    ```
