import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'services')))

from arxiv_service import fetch_arxiv_entries
from semanticscholar_service import fetch_citation_count

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    prefix = request.form['prefix']
    query = request.form['query']
    entries = fetch_arxiv_entries(prefix, query)
    
    results = []
    for entry in entries:
        result = process_entry(entry)
        results.append(result)
    
    sorted_results = sorted(results, key=lambda x: x['citation'], reverse=True)
    
    return render_template('results.html', results=results, sorted_results=sorted_results)

def process_entry(entry):
    id = entry.id.text.split("/")[-1].split("v")[0]
    title = entry.title.text
    summary = entry.summary.text
    authors = [author.find('name').text for author in entry.find_all('author')]
    link = entry.id.text
    citation = fetch_citation_count(id)
    return {'id': id, 'title': title, 'summary': summary, 'authors': authors, 'link': link, 'citation': citation}

if __name__ == '__main__':
    app.run(debug=True)
