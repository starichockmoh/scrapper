import sqlite3
import requests
import re

def remove_html_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text

conn = sqlite3.connect("neolurk.db")
cursor = conn.cursor()

cursor.execute("SELECT id, title, content, date FROM articles")
rows = cursor.fetchall()

ES_URL = "http://localhost:9200/articles/_doc"

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
