import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_research_plan(query: str) -> dict:
    """
    Uses Gemini to analyze the user's research query and generate a structured 
    research plan, breaking the main question down into specific search queries.
    
    Args:
        query: The user's original research question.
        
    Returns:
        dict: A parsed JSON dictionary containing:
              - 'understanding': A brief summary of what the user is looking for.
              - 'search_queries': A list of optimized search terms for the ArXiv API.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your environment.")

    # Initialize Gemini Model
    # We use a slightly higher temperature here for creative query optimization
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
    )

    prompt_template = """
You are an expert Autonomous Research Planner. Your goal is to take a broad research question from a user and break it down into an actionable research plan.

Research Question:
{query}

Your task is to:
1. Briefly state your understanding of the core topic.
2. Generate 2 to 3 optimized, distinct search queries that can be fed into an academic database (like ArXiv) to retrieve the most relevant literature. Keep the search queries concise (2-4 words maximum) for better API keyword matching.

You MUST return your response as a raw JSON object with the following schema:
{{
  "understanding": "String explaining the core focus",
  "search_queries": ["query 1", "query 2", "query 3"]
}}

Return ONLY valid JSON. Do not include markdown formatting blocks (like ```json), just the raw JSON text.
"""

    prompt = PromptTemplate(
        input_variables=["query"],
        template=prompt_template
    )

    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({"query": query})
    
    try:
        # Clean up potential markdown formatting if the LLM ignores instructions
        clean_response = response.replace("```json", "").replace("```", "").strip()
        plan_data = json.loads(clean_response)
        return plan_data
    except Exception as e:
        print(f"Failed to parse Planner JSON response: {response}")
        # Return a robust fallback
        return {
            "understanding": "Fallback to direct query search.",
            "search_queries": [query] 
        }

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set in your environment variables
    # import os; os.environ["GOOGLE_API_KEY"] = "your_key"
    
    test_query = "What are the latest applications of Multi-Agent reinforcement learning in robotic swarms?"
    try:
        print(f"Original Query: {test_query}\n")
        plan = generate_research_plan(test_query)
        print("--- Generated Research Plan ---")
        print(f"Understanding: {plan['understanding']}")
        print(f"Optimized Search Queries: {plan['search_queries']}")
    except Exception as e:
        print(f"Planner failed: {e}\n(Did you remember to set your GOOGLE_API_KEY?)")
