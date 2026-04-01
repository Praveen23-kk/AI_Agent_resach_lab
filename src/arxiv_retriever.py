import arxiv

def fetch_arxiv_papers(query: str, max_results: int = 5):
    """
    Searches ArXiv for the given query and returns a list of paper metadata and abstracts.
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    papers = []
    # Fetch results from the ArXiv API
    for result in client.results(search):
        # We extract title, authors, summary (abstract), and URL. 
        # In a more advanced implementation we could download the PDF instead.
        papers.append({
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "abstract": result.summary,
            "url": result.entry_id,
            "pdf_url": result.pdf_url
        })
    
    return papers
