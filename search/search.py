import requests
import re
import pymorphy3
ES_URL = "http://localhost:9200/articles/_search"

morph = pymorphy3.MorphAnalyzer()

def lemmatize_text(text):
    words = text.split()
    lemmatized_words = [morph.parse(word)[0].normal_form for word in words]
    return " ".join(lemmatized_words)


def search_articles(query, page, page_size):
    # Расчет отступа (с какого документа начинать)
    from_ = (page - 1) * page_size
    normalized_query = lemmatize_text(query)

    """Ищет статьи в Elasticsearch"""
    payload = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": normalized_query,
                            "fields": ["title^5", "lemmatize_content^2"],
                            "boost": 2
                        }
                    },
                    {
                        "multi_match": {
                            "query": normalized_query,
                            "fields": ["title^3", "lemmatize_content"],
                            "fuzziness": "AUTO",
                            "boost": 1
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        },
        "highlight": {
            "fields": {
                "lemmatize_content": {
                    "fragment_size": 200,
                    "number_of_fragments": 50
                }
            }
        },
        "from": from_,
        "size": page_size
    }

    response = requests.get(ES_URL, json=payload, headers={"Content-Type": "application/json"})
    data = response.json()

    # Вывод результатов
    hits = data.get("hits", {}).get("hits", [])
    if not hits:
        print("Ничего не найдено.")
        return [], 0

    print(f"Найдено всего {data['hits']['total']['value']}.\n")

    for hit in hits:
        print(f"✳️ {hit['_source']['title']} ({hit['_source']['date']}) score: {hit['_score']} id: {hit['_id']}")
        snippet = hit.get("highlight", {}).get("lemmatize_content", ["..."])[0]
        snippet = highlight_em(snippet)
        print(f"Content: {snippet}")
        print(f"Date: {hit['_source']['date']}")
        print("-" * 50)

    total_hits = data['hits']['total']['value']
    total_pages = (total_hits // page_size) + (1 if total_hits % page_size > 0 else 0)

    return hits, total_pages


def highlight_em(text):
    """Функция для выделения слов, обернутых в тег <em> красным цветом"""
    # ANSI escape-код для красного цвета текста
    green = "\033[32m"
    reset = "\033[0m"

    # Найдем все слова, заключенные в тег <em> и обернем их в красный цвет
    highlighted_text = re.sub(r'<em>(.*?)</em>', f'{green}\\1{reset}', text)

    return highlighted_text

def pagination_ui(query, page_size=10):
    page = 1
    while True:
        hits, total_pages = search_articles(query, page=page, page_size=page_size)

        if not hits:
            return

        print(f"\nСтраница {page} из {total_pages}")
        if page > 1:
            print(f"Предыдущая страница: {page - 1}")
        if page < total_pages:
            print(f"Следующая страница: {page + 1}")

        action = input("\nВыбор действия:\n1. Следующая страница\n2. Предыдущая страница\n3. Новый поиск\n4. Выход\n> ")

        if action == "1" and page < total_pages:
            page += 1
        elif action == "2" and page > 1:
            page -= 1
        elif action == "3":
            return  # Возвращаемся в основной цикл, где можно ввести новый запрос
        elif action == "4":
            print("Выходим...")
            break
        else:
            print("Че ввел")


if __name__ == "__main__":
    while True:
        query = input("Введите поисковый запрос: ")
        pagination_ui(query)
