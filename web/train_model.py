import os
import time
from elasticsearch import Elasticsearch
from datetime import datetime
from flask import jsonify

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize

el_cnn = 'elasticsearch:9200'
el_name = 'elastic'
el_pass = 'abc123456'

# Выгрузка запросов в текстовый файл
print("Выгрузка запросов...")
with open('queries.txt', 'w') as f:
    es = Elasticsearch([el_cnn], http_auth=(el_name, el_pass))
    query_body = {
        "query": {
            "match_all": {}
        }
    }
    results = es.search(index='suggests', body=query_body)
    for hit in results['hits']['hits']:
        f.write(f"{hit['_source']['query']}\n")
print("Выгрузка запросов завершена.")


# Обучение модели
print("Обучение модели...")
# time.sleep(10)  # Симуляция обучения модели
print("Обучение модели завершено.")