import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_novel_ideas(topic: str, context: str) -> dict:
    """
    Analyzes the provided topic and context to generate 5 novel, academic-ready
    research ideas using Gemini.
    
    Args:
        topic: The core research topic or query.
        context: Background information (typically retrieved via RAG).
        
    Returns:
        A structured JSON dictionary containing exactly 5 generated ideas.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your environment.")

    # Higher temperature (0.7) to encourage creativity and novel brainstorming
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7, 
    )

    prompt_template = """
You are a brilliant Senior academic AI researcher. Your task is to brainstorm 5 NOVEL, INNOVATIVE, and FEASIBLE academic research ideas based on the provided topic and context.

Research Topic:
{topic}

Context / Existing State of the Art:
{context}

Your generated ideas must logically build upon or challenge the gaps identified in the context. They should be rigorous enough for a Master's or PhD-level academic thesis.

You MUST return your response as a raw JSON object matching the exact schema below. Do not include markdown formatting blocks (like ```json).

{{
  "ideas": [
    {{
      "Title": "A catchy, academic title for the paper",
      "Problem_Statement": "What is the core hypothesis or problem being solved? (2-3 sentences max)",
      "Proposed_Method": "What specific algorithm, architecture, or methodological approach do you propose?",
      "Suggested_Dataset": "What existing datasets, or synthetic data generation methods, could be used?",
      "Expected_Impact": "Why does this matter? What is the academic or real-world benefit?"
    }}
  ]
}}

Generate exactly 5 ideas in the "ideas" array. Return ONLY valid JSON text.
"""

    prompt = PromptTemplate(
        input_variables=["topic", "context"],
        template=prompt_template
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({
        "topic": topic,
        "context": context
    })

    try:
        clean_response = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_response)
        return data
    except Exception as e:
        print(f"Failed to parse LLM JSON for Ideas Generator: {e}\nRaw Response: {response}")
        # Return fallback
        return {
            "ideas": [
                {
                    "Title": "Failed to generate ideas.",
                    "Problem_Statement": "JSON parsing error occurred.",
                    "Proposed_Method": "N/A",
                    "Suggested_Dataset": "N/A",
                    "Expected_Impact": "N/A"
                }
            ]
        }
