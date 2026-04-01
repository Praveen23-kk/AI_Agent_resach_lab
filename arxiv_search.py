import arxiv
import logging
from typing import List, Dict, Any

# Configure basic logging for error handling
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def search_papers(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search research papers using the ArXiv API.
    
    Args:
        query (str): The search term or topic (e.g., 'Agentic AI').
        max_results (int): Maximum number of papers to retrieve. Default is 5.
        
    Returns:
        List[Dict]: A list of dictionaries, each containing the paper's 
                    title, abstract, authors, and PDF link.
    """
    papers = []
    
    try:
        # Initialize ArXiv client with a safe page_size to prevent 400 Bad Request on broad queries
        client = arxiv.Client(page_size=max_results, delay_seconds=1.0, num_retries=3)
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        # Generator for fetching results
        for result in client.results(search):
            paper_info = {
                "title": result.title,
                "abstract": result.summary.replace('\n', ' '), # Clean up multiline returns
                "authors": [author.name for author in result.authors],
                "pdf_link": result.pdf_url
            }
            papers.append(paper_info)
            
        logging.info(f"Successfully retrieved {len(papers)} papers for query: '{query}'")
        
    except arxiv.ArxivError as e:
        logging.error(f"Failed to fetch from ArXiv API: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during the search: {e}")
        
    return papers

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Define a test query
    test_query = "Large Language Models Reasoning"
    print(f"Searching ArXiv for: '{test_query}'...\n")
    
    # Call the search function
    results = search_papers(test_query, max_results=3)
    
    # Display the results
    if results:
        for i, paper in enumerate(results, start=1):
            print(f"--- Paper {i} ---")
            print(f"Title: {paper['title']}")
            print(f"Authors: {', '.join(paper['authors'])}")
            print(f"PDF Link: {paper['pdf_link']}")
            print(f"Abstract Snippet: {paper['abstract'][:150]}...\n")
    else:
        print("No papers found or an error occurred during the search.")
