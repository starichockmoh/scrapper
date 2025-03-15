import sqlite3
import requests
import re
import pymorphy3

def remove_html_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text

morph = pymorphy3.MorphAnalyzer()

def lemmatize_text(text):
    words = text.split()
    lemmatized_words = [morph.parse(word)[0].normal_form for word in words]
    return " ".join(lemmatized_words)

conn = sqlite3.connect("../neolurk_scraper/neolurk.db")
cursor = conn.cursor()

cursor.execute("SELECT id, title, content, date FROM articles")
rows = cursor.fetchall()

ES_URL = "http://localhost:9200/articles/_doc"

for row in rows:
    cleaned_text = remove_html_tags(row[2])
    doc = {
        "id": row[0],
        "title": row[1],
        "content": cleaned_text,
        "lemmatize_content": lemmatize_text(cleaned_text),
        "date": row[3]
    }
    response = requests.post(f"{ES_URL}/{row[0]}", json=doc, headers={"Content-Type": "application/json"})
    print(response.json())

conn.close()
