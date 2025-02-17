from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

ARXIV_API_URL = "http://export.arxiv.org/api/query?search_query={}:{}&start=0&max_results=10"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    prefix = request.form['prefix']
    query = request.form['query']
    print(ARXIV_API_URL.format(prefix, query))
    response = requests.get(ARXIV_API_URL.format(prefix, query))
    print(response.status_code)
    if response.status_code != 200:
        return f"API request failed with status code {response.status_code}"
    
    soup = BeautifulSoup(response.content, features="xml")
    entries = soup.find_all('entry')
    print(f"Found {len(entries)} entries")
    
    results = []
    for entry in entries:
        id = entry.id.text.split("/")[-1].split("v")[0]
        title = entry.title.text
        summary = entry.summary.text
        authors = [author.find('name').text for author in entry.find_all('author')]
        link = entry.id.text
        try:
            sem = requests.get("https://api.semanticscholar.org/v1/paper/arXiv:"+id).json()
            citation = len(sem["citations"])
        except:
            citation = 0
        results.append({'id': id, 'title': title, 'summary': summary, 'authors': authors, 'link': link, 'citation': citation})
    
    # 引用数でソート
    sorted_results = sorted(results, key=lambda x: x['citation'], reverse=True)
    
    return render_template('results.html', results=sorted_results)

if __name__ == '__main__':
    app.run(debug=True)
