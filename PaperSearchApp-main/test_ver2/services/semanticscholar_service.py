import requests

SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/v1/paper/arXiv:{}"

def fetch_citation_count(arxiv_id):
    try:
        response = requests.get(SEMANTIC_SCHOLAR_API_URL.format(arxiv_id))
        if response.status_code != 200:
            raise Exception(f"Semantic Scholar API request failed with status code {response.status_code}")
        data = response.json()
        return len(data.get("citations", []))
    except:
        return 0
