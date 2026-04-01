import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.vector_store import get_vector_store

def get_rag_chain():
    """
    Constructs the conversational RAG chain using the Gemini API 
    and the ChromaDB retriever.
    """
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    # Init Retriever from Vector database
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    
    # System Instruction sets the personality and instructions for RAG synthesis
    system_prompt = (
        "You are an expert AI research assistant. Use the following pieces of retrieved "
        "academic context to answer the user's question. If you don't know the answer "
        "based on the context, say that you don't know rather than creating hallucinations.\n"
        "Provide insightful summaries, synthesize the points where helpful, and "
        "always cite the paper titles when deriving conclusions.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

def generate_insights(question: str) -> str:
    """
    Runs the RAG chain to generate an answer for the user's question.
    """
    rag_chain = get_rag_chain()
    response = rag_chain.invoke({"input": question})
    return response["answer"]
