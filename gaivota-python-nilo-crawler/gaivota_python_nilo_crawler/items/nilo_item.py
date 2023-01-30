import scrapy
from gaivota_crawler_driver.crawler.tools.database.item import DBUtilItem


class NiloItem(DBUtilItem):
    _schema = "registry_layers"  # DB schema
    _table = "nilo_imovel"  # DB table
    _id_columns = ['code']  # Columns to uniquely identify an item
    _excluded_columns_on_hash = ["s3_path"]  # Columns that should be disregarded when generating the item's hash

    _geo_columns = []  # Columns with geometry

    code = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    finalidade = scrapy.Field()
    area_total = scrapy.Field()
    url = scrapy.Field()
    cidade = scrapy.Field()
    estado = scrapy.Field()
    # description = scrapy.Field()
    features_contain = scrapy.Field()
    s3_path = scrapy.Field()
