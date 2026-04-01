# Agentic Research Lab

An autonomous AI research assistant designed to accelerate academic exploration. This system takes complex research questions, employs an AI planner to formulate optimal search strategies, fetches relevant papers via the ArXiv API, stores them in a ChromaDB vector database, and synthesizes highly structured insights, comparisons, and novel ideas using Gemini models with LangChain RAG architecture.

## 🚀 Features

- **Autonomous Research Pipeline:** Feed it a research question, and the system's "Planner Agent" will automatically decompose it into optimized sub-queries, gather research, and write a comprehensive markdown synthesis.
- **Dual Interface:** 
  - A clean, minimal UI powered by **Streamlit**.
  - A robust **FastAPI** backend supporting JSON-based API interactions, meant to be consumed by a modern **React/Vite** frontend.
- **Advanced Agentic Capabilities:**
  - **Planner Agent (`planner_agent.py`):** Breaks down complex questions into targeted search queries.
  - **Analysis Agent (`analysis_agent.py`):** Synthesizes insights and generates detailed markdown reports.
  - **Compare Agent (`compare_agent.py`):** Structurally compares the methodology, dataset, and findings of two distinct research papers.
  - **Idea Generator (`idea_generator.py`):** Suggests novel, academic-ready research topics based on provided context.
- **RAG Architecture:** Leverages ChromaDB for efficient semantic vector storage and retrieval of academic abstracts, paired with Google Gemini embeddings and LLMs for generation.

## 📁 Repository Structure

```text
├── .env.example               # Template for environment variables
├── README.md                  # Project overview and instructions
├── requirements.txt           # Python dependencies for the backend / Streamlit
├── app.py                     # Streamlit frontend application
├── main.py                    # FastAPI backend server
├── research_pipeline.py       # Core autonomous agentic pipeline orchestration
├── *_agent.py                 # Various agent implementations (planner, analysis, compare, etc.)
├── arxiv_search.py            # API integration for fetching papers from ArXiv
├── vector_store.py            # ChromaDB initialization and document ingestion logic
├── retriever.py               # RAG context retrieval logic
└── frontend/                  # React + Vite frontend application
    ├── package.json
    └── src/
```

## 🛠️ Setup Instructions

### 1. Prerequisites and Environment

1. **Clone the repository** and navigate to the project root.
2. **Set up a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   - Copy `.env.example` to `.env`.
   - Add your Google Gemini API key: `GOOGLE_API_KEY=your_api_key_here`.

### 2. Running the Streamlit Interface

The Streamlit app provides an immediate, user-friendly interface to test the autonomous research pipeline.

```bash
streamlit run app.py
```

### 3. Running the FastAPI Backend

If you wish to use the JSON REST API or connect the React frontend, start the FastAPI server:

```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can view the API documentation at `http://127.0.0.1:8000/docs`.

### 4. Running the React Frontend (Optional)

To run the Vite+React web application interacting with the FastAPI backend:

```bash
cd frontend
npm install
npm run dev
```

## 🧠 Core File Descriptions

- **`app.py`**: The Streamlit entry point. Combines planning, fetching, and reporting into a visual dashboard.
- **`main.py`**: The FastAPI application exposing endpoints like `/research`, `/compare`, and `/research-ideas`.
- **`research_pipeline.py`**: The central orchestrator that calls the planner, retriever, and analysis agents in sequence.
- **`arxiv_search.py` / `src/arxiv_retriever.py`**: Connects to the ArXiv API to query and download metadata for academic papers based on the planner's output.
- **`vector_store.py`**: Handles inserting `Document` representations into a persistent ChromaDB instance (`chroma_db_data/`).
```
