import scrapy


class MacbookItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
    price = scrapy.Field()
