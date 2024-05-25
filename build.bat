@echo off
echo Building FScrawler image...
docker build -t ls6-fscrawler-image .\crawler

echo Building Elasticsearch image...
docker build -t ls6-elasticsearch-image .\database

echo Building Web Interface image...
docker build -t ls6-web-image .\web

echo Building Suggestions Service image...
docker build -t ls6-suggestions-image .\suggestions

echo All images have been built successfully.
