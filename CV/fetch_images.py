import sqlite3
import os
import requests
from urllib.parse import urlparse
import re

# Укажите путь к вашей базе данных SQLite
db_path = 'neolurk.db'
# Папка, в которую будут сохранены изображения
save_folder = 'downloaded_images_urls'

# Подключаемся к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получаем первые 10 записей из таблицы articles
cursor.execute("SELECT image_urls FROM articles LIMIT 1000")
image_urls = cursor.fetchall()

# Создаем папку, если она не существует
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Скачиваем изображения
for idx, (urls_str,) in enumerate(image_urls):
    # Разбиваем строки с ссылками по запятой
    urls = urls_str.split(', ')

    for i, url in enumerate(urls):
        try:
            # Получаем содержимое изображения
            response = requests.get(url)
            response.raise_for_status()  # Если статус код не 200, будет исключение

            # Получаем имя файла из URL (извлекаем название файла из конца URL)
            path = urlparse(url).path
            file_name = os.path.basename(path)

            # Проверим, если файл имеет правильное расширение
            if not re.match(r'.*\.(jpg|jpeg|png|gif|bmp)$', file_name, re.IGNORECASE):
                print(f"Пропускаем файл с неподдерживаемым расширением: {file_name}")
                continue

            file_path = os.path.join(save_folder, file_name)

            # Сохраняем изображение в файл
            with open(file_path, 'wb') as f:
                f.write(response.content)

            print(f"Скачано: {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании {url}: {e}")

# Закрываем соединение с базой данных
conn.close()
