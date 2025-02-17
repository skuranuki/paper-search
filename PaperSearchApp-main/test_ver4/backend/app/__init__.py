from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from bs4 import BeautifulSoup
import requests
import logging
import concurrent.futures
import time
import threading

db = SQLAlchemy()
cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///VIEW_COUNT.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CACHE_TYPE'] = 'simple'  # Choose an appropriate caching type
    app.config['CACHE_DEFAULT_TIMEOUT'] = 259200  # Default cache timeout (3 days)

    db.init_app(app)
    cache.init_app(app)

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    class View_count(db.Model):
        id = db.Column(db.String(50), primary_key=True)
        link = db.Column(db.String(200), nullable=False)
        count = db.Column(db.Integer, default=0)

        def __repr__(self):
            return f'<View_count {self.id}: {self.count}>'

    with app.app_context():
        db.create_all()

    ARXIV_API_URL = "http://export.arxiv.org/api/query?search_query={}:{}&start=0&max_results=40"
    arxiv_lock = threading.Lock()
    last_request_time = 0

    @app.route('/')
    def home():
        return send_from_directory(app.template_folder, 'index.html')

    @app.route('/api/search', methods=['POST'])
    def search():
        nonlocal last_request_time

        data = request.json
        prefix = data['prefix']
        query = data['query']
        
        # Generate a cache key based on prefix and query
        cache_key = f"{prefix}_{query}"
        
        # キャッシュがあるか確認
        cached_result = cache.get(cache_key)
        if cached_result:
            # キャッシュがあっても閲覧数情報はデータベースから取得
            ids = [result['id'] for result in cached_result]
            view_counts = {vc.id: vc.count for vc in View_count.query.filter(View_count.id.in_(ids)).all()}
            for result in cached_result:
                result['view'] = view_counts.get(result['id'], 0)
            return jsonify(cached_result)

        # APIの使用間隔を3秒以上空ける
        with arxiv_lock:
            current_time = time.time()
            time_since_last_request = current_time - last_request_time
            if time_since_last_request < 3:
                time.sleep(3 - time_since_last_request)
            last_request_time = time.time()

        # キャッシュがない場合はAPI接続
        response = requests.get(ARXIV_API_URL.format(prefix, query))
        if response.status_code != 200:
            return jsonify({"error": f"API request failed with status code {response.status_code}"}), response.status_code

        soup = BeautifulSoup(response.content, features="xml")
        entries = soup.find_all('entry')

        def process_entry(entry):
            id = entry.id.text.split("/")[-1].split("v")[0]
            title = entry.title.text
            summary = entry.summary.text
            authors = [author.find('name').text for author in entry.find_all('author')]
            link = entry.id.text
            try:
                sem = requests.get(f"https://api.semanticscholar.org/v1/paper/arXiv:{id}").json()
                citation = len(sem.get("citations", []))
            except Exception as e:
                logger.exception(f"Exception occurred while fetching citations for {id}: {e}")
                citation = 0
            return {'id': id, 'title': title, 'summary': summary, 'authors': authors, 'link': link, 'citation': citation}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            partial_results = list(executor.map(process_entry, entries))

        ids = [result['id'] for result in partial_results]
        
        # Fetch view counts directly from the database every time
        view_counts = {vc.id: vc.count for vc in View_count.query.filter(View_count.id.in_(ids)).all()}

        results = []
        for result in partial_results:
            result['view'] = view_counts.get(result['id'], 0)
            results.append(result)

        sorted_results = sorted(results, key=lambda x: x['citation'], reverse=True)
        
        # Cache the result with the cache_key for 5 minutes
        cache.set(cache_key, sorted_results, timeout=259200)
        
        return jsonify(sorted_results)

    @app.route('/api/view_count', methods=['POST'])
    def view_count():
        data = request.json
        logger.debug('View count request received with data: %s', data)
        view_count = View_count.query.get(data['id'])
        if view_count:
            view_count.count += 1
        else:
            view_count = View_count(id=data['id'], link=data['link'], count=1)
            db.session.add(view_count)
        try:
            db.session.commit()
            logger.debug('View count logged successfully')
            return jsonify({'message': 'View count logged successfully'})
        except Exception as e:
            logger.exception('Exception occurred while committing to the database: %s', e)
            db.session.rollback()
            return jsonify({'error': 'Failed to log view count'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
