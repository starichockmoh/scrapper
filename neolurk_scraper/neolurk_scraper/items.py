import scrapy


class NeolurkScraperItem(scrapy.Item):
    title = scrapy.Field()      # Заголовок статьи
    content = scrapy.Field()    # Текст статьи
    image_urls = scrapy.Field()  # Список URL изображений
    url = scrapy.Field()        # URL статьи
    date = scrapy.Field()       # Дата публикации
