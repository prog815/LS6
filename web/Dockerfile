# Используем официальный образ Python в качестве базового образа
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения в рабочую директорию
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем cron
RUN apt-get update && apt-get install -y cron

# Задаем переменную среды для указания порта, на котором будет работать Flask
ENV PORT=5000

# Указываем команду для запуска скрипта обучения модели раз в день
RUN crontab -l | { cat; echo "* * * * * python train_model.py"; } | crontab -

# Указываем команду для запуска крона и Flask-приложения
CMD cron && python app.py