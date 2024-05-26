@echo off

REM Указываем путь к каталогу production
SET PRODUCTION_DIR=production

REM Создаем каталог production, если он не существует
IF NOT EXIST %PRODUCTION_DIR% mkdir %PRODUCTION_DIR%

echo Exporting crawler
docker save -o %PRODUCTION_DIR%\ls6-fscrawler-image.tar ls6-fscrawler-image

echo Exporting database
docker save -o %PRODUCTION_DIR%\ls6-elasticsearch-image.tar ls6-elasticsearch-image

echo Exporting web
docker save -o %PRODUCTION_DIR%\ls6-web-image.tar ls6-web-image

echo Exporting suggestions
docker save -o %PRODUCTION_DIR%\ls6-suggestions-image.tar ls6-suggestions-image

echo All images exported to %PRODUCTION_DIR% directory.

echo Coping files docker-compose.yml and .env
COPY docker-compose.yml %PRODUCTION_DIR%
COPY .env %PRODUCTION_DIR%

echo All files ready in %PRODUCTION_DIR% directory!!!