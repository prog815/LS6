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

# Load the text file with queries
queries = []
with open('queries.txt', 'r') as f:
    queries = [line.strip() for line in f.readlines()]

# Check if the list of queries is not empty
if not queries:
    print("List of queries is empty. Skipping training.")
    exit()

# Предобработка данных: токенизация
tokenized_data = [word_tokenize(phrase.lower()) for phrase in queries]
                  
# Подготовка данных в формате, подходящем для обучения Doc2Vec
tagged_data = [TaggedDocument(words=words, tags=[str(i)]) for i, words in enumerate(tokenized_data)]
                
# Обучение модели
print("Обучение модели...")

model = Doc2Vec(vector_size=100, window=5, min_count=1, workers=4, epochs=20)
model.build_vocab(tagged_data)
model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
model.save('model.bin')

print("Обучение модели завершено.")