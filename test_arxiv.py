import arxiv

queries = [
    "ai",
    "artificial intelligence",
    "all:ai",
    '"ai"',
    "abs:ai"
]

client = arxiv.Client()

for q in queries:
    print(f"Testing query: {q}")
    search = arxiv.Search(query=q, max_results=2)
    try:
        results = list(client.results(search))
        print(f"  Success: {len(results)} results")
    except Exception as e:
        print(f"  Failed: {e}")
