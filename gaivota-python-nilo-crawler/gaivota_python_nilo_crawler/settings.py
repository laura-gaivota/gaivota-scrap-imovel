import os

DEBUG = os.getenv("DEBUG")
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 50
TELNETCONSOLE_ENABLED = False
SPIDER_MIDDLEWARES = {
    "gaivota_crawler_driver.crawler.middlewares.GaivotaLogger": 100,
}
# DOWNLOADER_MIDDLEWARES = {
#     "gaivota_crawler_driver.crawler.middlewares.GaivotaProxy": 0,
# }
ITEM_PIPELINES = {
    "gaivota_crawler_driver.crawler.pipelines.DBUtilHashCheckPipeline": 1
}
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = list(range(400, 510))
LOG_LEVEL = "INFO"
SPIDER_MODULES = ["gaivota_python_nilo_crawler.spiders"]
