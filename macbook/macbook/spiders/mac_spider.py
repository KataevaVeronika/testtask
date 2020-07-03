import scrapy
import os
import requests


def parse_page(response):
    parent = os.path.abspath('..') + '\\tmp\\'
    title = response.xpath('//h1[@class = "it-ttl"]/text()').extract()[0]
    image = response.xpath('//img[@id="icImg"]//@src').extract()[0]
    filename_html = title + '.html'
    img_ext = "." + image.split(".")[-1]
    filename_img = title + img_ext
    with open(parent + filename_html.replace('"', '').replace('/', ''), 'wb') as f:
        f.write(response.body)
    with open(parent + filename_img.replace('"', '').replace('/', ''), 'wb') as f:
        image = requests.get(image)
        f.write(image.content)


class MacSpider(scrapy.Spider):
    name = "mac"
    start_urls = [
        'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.'
        'H0.XMacbook.TRS1&_nkw=Macbook+Pro+13&_sacat=0',
    ]

    def parse(self, response):
        prices = response.xpath('//span[@class = "s-item__price"]/text()')\
                         .extract()
        # price formatting was executed according to the way numbers are displayed in Russian ebay
        prices = [float(price.replace('\xa0', '').replace(',', '.')[:-5:])
                  for price in prices]
        hrefs = response.xpath('//a[@class = "s-item__link"]/@href').extract()
        lowest = sorted(zip(prices, hrefs), reverse=False)[:3:]
        for laptop in lowest:
            yield scrapy.Request(laptop[1], callback=parse_page)
