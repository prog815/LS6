from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import logging
from datetime import datetime
import time
import os
from flask import jsonify
from gensim.models import Doc2Vec
from nltk.tokenize import word_tokenize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

el_cnn = 'elasticsearch:9200'
el_name = 'elastic'
el_pass = 'abc123456'

queries = []
model = None
last_update_time = 0

def search_in_elasticsearch(query, page=1, page_size=10):
    # Создайте подключение к Elasticsearch
    es = Elasticsearch([el_cnn], http_auth=(el_name, el_pass))

    # Определите запрос для Elasticsearch
    body = {
        "_source": [],
        "from": (page - 1) * page_size,
        "size": page_size,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["content"]
            }
        },
        "highlight": {
            "fields": {
                "content": {}
            }
        }
    }

    # Выполните поиск в Elasticsearch
    logger.info(body)
    results = es.search(index="idx", body=body)
    # logger.info(results)

    # Верните результаты
    return results['hits']['hits']

def count_pages(query, page_size=10):
    es = Elasticsearch([el_cnn], http_auth=(el_name, el_pass))

    count_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["content"]
            }
        }
    }

    count_results = es.count(index="idx", body=count_body)
    total_results = count_results['count']

    total_pages = (total_results + page_size - 1) // page_size

    return total_pages

def log_search_query(query, page_number, client_ip):
    es = Elasticsearch([el_cnn], http_auth=(el_name, el_pass))

    doc = {
        'query': query,
        'page_number': page_number,
        'client_ip': client_ip,
        'timestamp': datetime.now()
    }

    es.index(index='suggests', body=doc)
    logger.info(f"Logged search query: {doc}")


app = Flask(__name__)

# --------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    logger.info('home')
    if request.method == 'GET':
        query = request.args.get('query', default="", type=str)

        page_number = request.args.get('page', default=1, type=int)
        page_size = 10  # Размер страницы
        total_pages = count_pages(query, page_size=page_size)

        if page_number < 1 or page_number > total_pages:
            page_number = 1
            
        client_ip = request.remote_addr

        logger.info("search")

        results = search_in_elasticsearch(query, page=page_number, page_size=page_size)

        logger.info(len(results))
        
        # Log the search query
        log_search_query(query, page_number, client_ip)

        return render_template('index.html', results=results, query=query, current_page=page_number, total_pages=total_pages)
    return render_template('index.html')

# --------------------------------------------------------------

@app.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('query', default="", type=str)
    suggested_terms = generate_suggestions(query)
    return jsonify(suggested_terms)

def generate_suggestions(query, num_suggestions=10):
    """
    Генерирует список подсказок.
    """
    
    global queries, model, last_update_time
    
    try:
        # Проверка времени последнего обновления
        if time.time() - last_update_time > 3600:
            # Обновление списка запросов
            queries = []
            with open('queries.txt', 'r') as f:
                queries = [line.strip() for line in f.readlines()]

            # Обновление модели
            model = Doc2Vec.load('model.bin')

            # Обновление времени последнего обновления
            last_update_time = time.time()
        
        # Токенизация запроса
        query_tokens = word_tokenize(query.lower().strip().replace('  ', ' '))
        
        # Вектор для запроса
        query_vector = model.infer_vector(query_tokens)
        
        # Наиболее похожие фразы
        similar_phrases = model.dv.most_similar([query_vector], topn=10)
        
        suggestions = [f"{queries[int(index)]}" for index, score in similar_phrases]
        
        return suggestions
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
