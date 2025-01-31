import scrapy
import json
from pathlib import Path
from neolurk_scraper.items import NeolurkScraperItem

class NeolurkSpider(scrapy.Spider):
    name = "neolurk"
    allowed_domains = ["neolurk.org"]
    start_urls = ["https://neolurk.org/wiki/%D0%92%D0%B5%D1%80%D1%85%D0%BD%D1%8F%D1%8F_%D0%92%D0%BE%D0%BB%D1%8C%D1%82%D0%B0_%D1%81_%D1%80%D0%B0%D0%BA%D0%B5%D1%82%D0%B0%D0%BC%D0%B8"]  # Начальная точка сканирования

    def __init__(self, *args, **kwargs):
        super(NeolurkSpider, self).__init__(*args, **kwargs)
        # Загружаем существующие заголовки из output.json
        self.existing_titles = self.load_existing_titles()
        print("Titles ara", list(self.existing_titles))

    def load_existing_titles(self):
        # Проверяем, существует ли файл output.json
        file_path = Path("output.json")
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    # Извлекаем все заголовки из файла
                    return {item["title"] for item in data}
                except json.JSONDecodeError:
                    # Если файл пустой или поврежден, возвращаем пустое множество
                    print('error!!!! JSONDecodeError')
                    return set()
        print('error!!!!')
        return set()

    def parse(self, response):
        # Находим ссылки на статьи
        articles = response.xpath('//a[contains(@href, "/wiki/")]/@href').getall()
        for article in articles:
            full_url = response.urljoin(article)
            if '/wiki/Категория:' in article:
                yield scrapy.Request(full_url, callback=self.parse)
                # Если это статья, парсим её
            else:
                yield scrapy.Request(full_url, callback=self.parse_article)

    def parse_article(self, response):
        # Извлечение данных статьи
        item = NeolurkScraperItem()
        item['title'] = response.xpath('//h1/text()').get().strip()
        if item['title'] in self.existing_titles:
            self.logger.info(f"Статья уже обработана: {item['title']}")
            return  # Пропускаем статью, если она уже есть в output.json
        content = " ".join(response.xpath('//div[@class="mw-parser-output"]//p//text()').getall()).strip()
        item['content'] = content
        item['url'] = response.url
        # Извлечение URL изображений (атрибут src из тега <img>)
        item['image_urls'] = response.xpath('//div[@class="mw-parser-output"]//img/@src').getall()
        # Преобразование относительных ссылок на изображения в абсолютные
        item['image_urls'] = [response.urljoin(url) for url in item['image_urls']]
        item['date'] = response.xpath('//li[@id="footer-info-lastmod"]/text()').re_first(r'\d{1,2} \w+ \d{4}')
        if content != " " and content != "":
            yield item
