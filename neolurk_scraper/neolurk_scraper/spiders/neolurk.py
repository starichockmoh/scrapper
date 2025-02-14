import scrapy
import json
from pathlib import Path
from neolurk_scraper.items import NeolurkScraperItem

class NeolurkSpider(scrapy.Spider):
    name = "neolurk"
    allowed_domains = ["neolurk.org"]
    start_urls = ["https://neolurk.org/wiki/%D0%94%D0%BE%D0%B1%D1%80%D1%8B%D0%B5_%D0%B0%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B0%D0%BD%D1%86%D1%8B"]  # Начальная точка сканирования

    def __init__(self, *args, **kwargs):
        super(NeolurkSpider, self).__init__(*args, **kwargs)
        # Загружаем существующие заголовки из output.json
        self.existing_titles = self.load_existing_titles()

    def load_existing_titles(self):
        # Проверяем, существует ли файл output.json
        file_path = Path("output.json")
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return {item["title"] for item in data}
                except json.JSONDecodeError:
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
        item = NeolurkScraperItem()
        item['title'] = response.xpath('//h1/text()').get().strip()
        if item['title'] in self.existing_titles:
            self.logger.info(f"Статья уже обработана: {item['title']}")
            return
        content = " ".join(response.xpath('//div[@class="mw-parser-output"]//p//text()').getall()).strip()
        item['content'] = content
        item['url'] = response.url
        # Извлечение URL изображений
        item['image_urls'] = response.xpath('//div[@class="mw-parser-output"]//img/@src').getall()
        # Преобразование относительных ссылок на изображения в абсолютные
        item['image_urls'] = [response.urljoin(url) for url in item['image_urls']]
        item['date'] = response.xpath('//li[@id="footer-info-lastmod"]/text()').re_first(r'\d{1,2} \w+ \d{4}')
        if content != " " and content != "":
            yield item
