# Используем официальный образ FScrawler
FROM dadoonet/fscrawler:2.7

# Устанавливаем рабочую директорию
WORKDIR /usr/share/fscrawler

# Копируем конфигурационные файлы FScrawler в образ
COPY config /root/.fscrawler

# Задаем команду запуска FScrawler
CMD ["fscrawler", "idx", "--restart"]
