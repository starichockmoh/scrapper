import sqlite3
import requests
import re
import json

def remove_html_tags(text):
    """Удаляем HTML теги с помощью регулярного выражения"""
    clean_text = re.sub(r'<.*?>', '', text)  # Убирает все HTML теги
    return clean_text

conn = sqlite3.connect("neolurk.db")  # замените на путь к вашей БД
cursor = conn.cursor()

cursor.execute("SELECT id, title, content, date FROM articles")
rows = cursor.fetchall()

# URL Elasticsearch
ES_URL = "http://localhost:9200/articles/_doc"

# Отправляем данные в Elasticsearch
for row in rows:
    doc = {
        "id": row[0],
        "title": row[1],
        "content": remove_html_tags(row[2]),
        "date": row[3]
    }
    response = requests.post(f"{ES_URL}/{row[0]}", json=doc, headers={"Content-Type": "application/json"})
    print(response.json())

conn.close()
