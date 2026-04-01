import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def compare_research_papers(paper_a: dict, paper_b: dict) -> dict:
    """
    Analyzes and compares two research papers using Gemini to extract key differences
    in methodology, datasets, strengths, limitations, and use cases.
    
    Args:
        paper_a: Dictionary containing 'title' and 'abstract'.
        paper_b: Dictionary containing 'title' and 'abstract'.
        
    Returns:
        A structured JSON dictionary containing the comparative analysis.
    """
    # Ensure API Key is available
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your environment.")

    # Initialize Gemini Model
    # Low temperature (0.1) for highly analytical, factual comparative output
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1, 
    )

    # Define a strong prompt template forcing structured JSON output
    prompt_template = """
You are an expert AI Research Scientist. Your task is to perform a rigorous comparative analysis of two different academic research papers based on their titles and abstracts. Your goal is to generate a concise, highly structured analysis suitable for display in a professional research dashboard.

=== Paper A ===
Title: {title_a}
Abstract: {abstract_a}

=== Paper B ===
Title: {title_b}
Abstract: {abstract_b}
================

Based ONLY on the provided abstracts, systematically compare these two papers. If an abstract lacks specific details for a category, infer logically or simply state "Not explicitly mentioned" instead of hallucinating.

You MUST return your response as a raw JSON object with exactly the following schema:

{{
  "comparison": {{
    "methodology_differences": "Briefly describe how their core approaches or architectures differ.",
    "datasets_used": "What datasets or environments did they use/evaluate on?",
    "key_contributions": "What is the primary breakthrough or novel contribution of each paper?",
    "strengths_of_each": "What are the contrasting strengths of Paper A vs Paper B?",
    "limitations": "What are the limitations or trade-offs of each?",
    "when_to_use_a_vs_b": "When would a practitioner choose Paper A's approach over Paper B's?"
  }}
}}

Return ONLY valid JSON text. Do not include markdown formatting blocks (like ```json).
"""

    prompt = PromptTemplate(
        input_variables=["title_a", "abstract_a", "title_b", "abstract_b"],
        template=prompt_template
    )

    chain = prompt | llm | StrOutputParser()

    # Execute the analysis
    response = chain.invoke({
        "title_a": paper_a.get("title", "Unknown Title"),
        "abstract_a": paper_a.get("abstract", "No Abstract Provided"),
        "title_b": paper_b.get("title", "Unknown Title"),
        "abstract_b": paper_b.get("abstract", "No Abstract Provided")
    })

    try:
        # Clean up potential markdown formatting if the LLM escapes instructions
        clean_response = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_response)
        return data
    except Exception as e:
        print(f"Failed to parse LLM JSON for comparison: {e}\nRaw Response: {response}")
        # Return a robust fallback matching the requested schema
        return {
            "comparison": {
                "methodology_differences": "Failed to parse analysis.",
                "datasets_used": "N/A",
                "key_contributions": "N/A",
                "strengths_of_each": "N/A",
                "limitations": "N/A",
                "when_to_use_a_vs_b": "N/A"
            }
        }
