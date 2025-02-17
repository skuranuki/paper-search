import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'services')))

from arxiv_service import fetch_arxiv_entries
from semanticscholar_service import fetch_citation_count

print("Import successful!")
