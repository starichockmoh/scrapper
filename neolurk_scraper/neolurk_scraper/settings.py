# Название бота (можете изменить)
BOT_NAME = "neolurk_scraper"

# Модули с пауками
SPIDER_MODULES = ["neolurk_scraper.spiders"]
NEWSPIDER_MODULE = "neolurk_scraper.spiders"

# Соблюдение правил robots.txt
ROBOTSTXT_OBEY = True  # Учитываем файл robots.txt

# Задержка между запросами
DOWNLOAD_DELAY = 2  # 2 секунды задержки между запросами

# Настройки параллельных запросов
CONCURRENT_REQUESTS = 16  # Общее количество запросов
CONCURRENT_REQUESTS_PER_DOMAIN = 8  # Запросы на домен
CONCURRENT_REQUESTS_PER_IP = 8  # Запросы с одного IP

# Логирование
LOG_LEVEL = "INFO"  # Логирование уровня INFO

# User-Agent для идентификации
USER_AGENT = "neolurk_scraper (+https://neolurk.org)"

# Автоматическое регулирование скорости запросов (AutoThrottle)
AUTOTHROTTLE_ENABLED = True  # Включить AutoThrottle
AUTOTHROTTLE_START_DELAY = 1  # Начальная задержка (в секундах)
AUTOTHROTTLE_MAX_DELAY = 10  # Максимальная задержка
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Среднее количество запросов одновременно
AUTOTHROTTLE_DEBUG = False  # Отключить подробный вывод троттлинга

# Настройка хранения данных (можно изменить на JSON, MongoDB, etc.)
FEEDS = {
    "output.json": {
        "format": "json",
        "encoding": "utf8",
        "store_empty": False,
        "indent": 4,
    },
}

# Пайплайны для обработки данных (добавляем, если нужно сохранить в базу)
ITEM_PIPELINES = {
    "neolurk_scraper.pipelines.SQLitePipeline": 300,  # Включаем сохранение в SQLite
}

# Настройки таймаутов
DOWNLOAD_TIMEOUT = 15  # Тайм-аут на загрузку страниц

# Отключение кэширования (по умолчанию включено в Scrapy)
HTTPCACHE_ENABLED = False
