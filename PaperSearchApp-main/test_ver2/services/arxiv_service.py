import requests
from bs4 import BeautifulSoup

ARXIV_API_URL = "http://export.arxiv.org/api/query?search_query={}:{}&start=0&max_results=10"

def fetch_arxiv_entries(prefix, query):
    response = requests.get(ARXIV_API_URL.format(prefix, query))
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    soup = BeautifulSoup(response.content, features="xml")
    return soup.find_all('entry')
