import sqlite3

class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("neolurk.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                image_urls TEXT,
                url TEXT UNIQUE,
                date TEXT
            )
        """)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # Преобразуем список URL изображений в строку (разделённую запятыми)
        image_urls = ", ".join(item['image_urls'])

        self.cursor.execute("SELECT url FROM articles WHERE url = ?", (item['url'],))
        existing_entry = self.cursor.fetchone()

        if existing_entry:
            spider.logger.info(f"Статья с URL {item['url']} уже существует в базе. Пропускаем.")
        else:
            self.cursor.execute('''
                    INSERT INTO articles (title, content, url, image_urls, date)
                    VALUES (?, ?, ?, ?, ?)
                ''', (item['title'], item['content'], item['url'], image_urls, item['date']))
            self.connection.commit()

        return item
