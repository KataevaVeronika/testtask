import scrapy
import os
import requests
import re


class MacSpider(scrapy.Spider):
    name = "mac"
    start_urls = [
        'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2540003.m570.l1312.R1.TR0.TRC0.A0.H1.TRS1&_nkw=Macbook+Pro+13&_sacat=0',
    ]
    def parse(self, response):

        def parse_page(response):
            parent = os.path.join(os.path.dirname(os.getcwd()), 'tmp/')
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

        prices = response.xpath('//span[@class = "s-item__price"]/text()')\
                         .extract()
        prices = [float(re.sub('[^\d\.]', '', price)) for price in prices]
        print(prices)

        hrefs = response.xpath('//a[@class = "s-item__link"]/@href').extract()
        lowest = sorted(zip(prices, hrefs), reverse=False)[:3:]
        print(lowest[0])
        print(lowest[1])
        print(lowest[2])
        for laptop in lowest:
            yield scrapy.Request(laptop[1], callback=parse_page)
