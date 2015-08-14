import scrapy
from fittinger.items import FittingerItem
__author__ = 'vvvkamper'


class MrPorterSpider(scrapy.Spider):
    name = 'mrporter'
    allowed_domains = ['mrporter.com']

    start_urls = [
        "http://www.mrporter.com/en-us/mens/clothing?viewall=on"
    ]

    def parse(self, response):
        for href in response.css("div#product-list div.product-image a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        # next_page = response.css("div:not(.last-page) a.next-page::attr('href')")
        # if len(next_page) > 0:
        #     next_page_url = response.urljoin(next_page[0].extract())
        #     yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_dir_contents(self, response):
        item = FittingerItem()
        product_details = response.css("div#product-details")
        item['name'] = product_details.css("h4::text").extract()[0]
        item['brand'] = product_details.css("h1::text").extract()[0]
        item['price'] = product_details.css("span.price > span::text").extract()[0]
        item['images'] = response.css("img#medium-image::attr('src')").extract()
        item['note'] = response.css("div.product-description > div").extract()[0]
        item['link'] = response.request.url
        yield item

        # for href in response.css("div#alternative-colors a::attr('href')"):
        #     url = response.urljoin(href.extract())
        #     yield scrapy.Request(url, callback=self.parse_dir_contents)