import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from dotenv import load_dotenv

# Import our existing pipeline modular functions
from arxiv_search import search_papers
from vector_store import add_documents
from retriever import retrieve_context
from compare_agent import compare_research_papers
from idea_generator import generate_novel_ideas

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Agentic Research Lab API",
    description="Backend API for querying ArXiv, embedding with ChromaDB, and synthesizing insights via Gemini RAG.",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------
class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    papers: List[Dict[str, Any]]
    summary: str
    research_gaps: str
    future_directions: str

class PaperBase(BaseModel):
    title: str
    abstract: str

class CompareRequest(BaseModel):
    paperA: PaperBase
    paperB: PaperBase

class ComparisonMetrics(BaseModel):
    methodology_differences: str
    datasets_used: str
    key_contributions: str
    strengths_of_each: str
    limitations: str
    when_to_use_a_vs_b: str

class CompareResponse(BaseModel):
    comparison: ComparisonMetrics

class IdeaRequest(BaseModel):
    topic: str
    context: str

class IdeaItem(BaseModel):
    Title: str
    Problem_Statement: str
    Proposed_Method: str
    Suggested_Dataset: str
    Expected_Impact: str

class IdeaResponse(BaseModel):
    ideas: List[IdeaItem]

# ---------------------------------------------------------
# Helper: JSON Generation Agent
# ---------------------------------------------------------
def generate_insights_json(query: str, context: str) -> dict:
    """
    Directly asks Gemini to return a structured JSON conforming to the API requirements.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("Google API key not found.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2, 
    )

    prompt_template = """
You are an expert AI research scientist. Your task is to analyze a set of retrieved academic research papers and answer the user's research question comprehensively.

Research Question:
{query}

Retrieved Context (Abstracts and Metadata):
{context}

Based ON THE CONTEXT above, provide a structured analysis. 

You MUST return your response as a raw JSON object with the following exact keys:
{{
  "summary": "Summarize the main discoveries and key trends.",
  "research_gaps": "Highlight missing areas, limits, or unanswered questions.",
  "future_directions": "Suggest potential areas for future exploration that build upon findings."
}}

Return ONLY valid JSON. Do not include markdown formatting blocks (like ```json), just the raw JSON text.
"""
    prompt = PromptTemplate(input_variables=["query", "context"], template=prompt_template)
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({"query": query, "context": context})
    
    try:
        clean_response = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_response)
        return data
    except Exception as e:
        print(f"Failed to parse LLM JSON: {e}")
        return {
            "summary": "Failed to parse analysis.",
            "research_gaps": "N/A",
            "future_directions": "N/A"
        }

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------
@app.post("/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):
    """
    Executes the research pipeline and returns a structured JSON.
    """
    query = request.query
    
    try:
        # 1. Search papers from ArXiv
        papers = search_papers(query=query, max_results=5)
        
        if not papers:
            return ResearchResponse(
                papers=[],
                summary="No papers found matching the query.",
                research_gaps="",
                future_directions=""
            )
            
        # 2. Store abstracts in ChromaDB
        add_documents(papers)
        
        # 3. Retrieve relevant context (top chunks)
        context = retrieve_context(query=query, top_k=4)
        
        if context == "No relevant context found in the vector database.":
             return ResearchResponse(
                papers=papers,
                summary="Failed to retrieve context from database.",
                research_gaps="",
                future_directions=""
            )
             
        # 4 & 5. Send context to Gemini and generate structured research insights
        insights = generate_insights_json(query=query, context=context)
        
        return ResearchResponse(
            papers=papers,
            summary=insights.get("summary", ""),
            research_gaps=insights.get("research_gaps", ""),
            future_directions=insights.get("future_directions", "")
        )
        
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare", response_model=CompareResponse)
async def compare_papers(request: CompareRequest):
    """
    Takes two distinct research papers and executes a structural comparison via Gemini.
    """
    try:
        # Convert Pydantic models to dicts for the agent
        paper_a_dict = {"title": request.paperA.title, "abstract": request.paperA.abstract}
        paper_b_dict = {"title": request.paperB.title, "abstract": request.paperB.abstract}
        
        # Call the new compare agent
        comparison_results = compare_research_papers(paper_a_dict, paper_b_dict)
        
        return CompareResponse(
            comparison=ComparisonMetrics(**comparison_results.get("comparison", {}))
        )
        
    except Exception as e:
        print(f"Server Error in Comparison: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research-ideas", response_model=IdeaResponse)
async def generate_ideas(request: IdeaRequest):
    """
    Generates 5 novel, academic-ready research ideas based on the provided topic and context.
    """
    try:
        ideas_data = generate_novel_ideas(topic=request.topic, context=request.context)
        return IdeaResponse(ideas=ideas_data.get("ideas", []))
    except Exception as e:
        print(f"Server Error in Ideas Generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "FastAPI AI Backend is running smoothly."}

# ==========================================
# Run Locally command: `uvicorn main:app --reload`
# ==========================================
