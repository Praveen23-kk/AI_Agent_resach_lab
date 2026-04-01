import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def analyze_papers(research_question: str, context: str) -> str:
    """
    Analyzes retrieved research papers using Gemini to extract key findings,
    trends, gaps, and future opportunities based on the research question.
    
    Args:
        research_question: The user's query or topic of interest.
        context: The concatenated string of abstracts and metadata retrieved from the vector database.
        
    Returns:
        A structured markdown string containing the 4 required analytical sections.
    """
    # Ensure API Key is available
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your environment.")

    # Initialize Gemini Model
    # We use a low temperature (0.2) to prioritize factual, analytical formatting 
    # over creative story-telling for academic analysis.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2, 
    )

    # Define a strong prompt template
    prompt_template = """
You are an expert AI research scientist. Your task is to analyze a set of retrieved academic research papers and answer the user's research question comprehensively.

Research Question:
{research_question}

Retrieved Context (Abstracts and Metadata):
{context}

Based ON THE CONTEXT PROVIDED above, please provide a structured analysis containing exactly the following four sections. If the context does not contain enough information for a specific section, state that explicitly based on the available data. Do not hallucinate external knowledge.

### 1. Key Findings
Summarize the main discoveries, methodologies, or results presented in the papers. Focus on what was achieved or proven.

### 2. Research Trends
Identify any common themes, shifting paradigms, or general directions the research is heading based on the provided papers. What patterns emerge across the studies?

### 3. Research Gaps
Highlight what is missing, unanswered questions, or limitations mentioned or evident in the current research context.

### 4. Future Research Opportunities
Suggest potential areas for future exploration or experiments that would build logically upon the current findings and address the identified gaps.

Your output must be formatted in clean Markdown, using the exact section headers provided above. Keep your analysis concise, academic, and highly structured.
"""

    prompt = PromptTemplate(
        input_variables=["research_question", "context"],
        template=prompt_template
    )

    # Create the LCEL chain (Prompt -> LLM -> Raw String Output)
    chain = prompt | llm | StrOutputParser()

    # Execute the analysis
    response = chain.invoke({
        "research_question": research_question,
        "context": context
    })

    return response

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # We use a dummy context as an example
    sample_question = "How are AI systems simulating believable human behavior?"
    sample_context = '''
--- Paper ---
Title: Generative Agents: Interactive Simulacra of Human Behavior
Authors: Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein
Link: https://arxiv.org/abs/2304.03442
Abstract: Believable proxies of human behavior can empower interactive applications ranging from immersive environments to rehearsal spaces for interpersonal communication to prototyping tools. In this paper, we introduce generative agents--computational software agents that simulate believable human behavior. Generative agents wake up, cook breakfast, and head to work; artists paint, while authors write; they form opinions, notice each other, and initiate conversations; they remember and reflect on days past as they plan the next day. To enable generative agents, we describe an architecture that extends a large language model to store a complete record of the agent's experiences using natural language, synthesize those memories over time into higher-level reflections, and retrieve them dynamically to plan behavior.

--- Paper ---
Title: Playing games with AI: simulating human behavior in Turing Tests
Authors: Jane Doe, John Smith
Link: No PDF Link
Abstract: This paper explores how large language models can be prompted to simulate different human personas during strategic gameplay, highlighting that while LLMs adapt well to persona prompts, their decision-making logic sometimes lacks the long-term context memory present in real human subjects.
    '''
    
    # Note: Needs GOOGLE_API_KEY environment variable to be set to run successfully.
    # import os; os.environ["GOOGLE_API_KEY"] = "YOUR_KEY_HERE"
    
    try:
        print(f"Question: '{sample_question}'")
        print("Analyzing context with Gemini...\n")
        
        analysis_report = analyze_papers(sample_question, sample_context)
        
        print(analysis_report)
    except Exception as e:
        print(f"Analysis failed: {e}\n(Did you remember to set your GOOGLE_API_KEY?)")
