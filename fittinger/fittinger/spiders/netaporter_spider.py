import scrapy
from fittinger.items import FittingerItem
__author__ = 'vvvkamper'


class NetaporterSpider(scrapy.Spider):
    name = 'netaporter'
    allowed_domains = ['net-a-porter.com']

    start_urls = [
        "http://www.net-a-porter.com/us/en/d/Shop/Clothing/All?cm_sp=topnav-_-clothing-_-allclothing&pn=1&npp=60&image_view=product&dscroll=0"
    ]

    def parse(self, response):
        for href in response.css("div#product-list > ul > li > div.description > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        next_page = response.css("div:not(.last-page) a.next-page::attr('href')")
        if len(next_page) > 0:
            next_page_url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_dir_contents(self, response):
        item = FittingerItem()
        product_details = response.css("div#product-details")
        item['name'] = product_details.css("h1::text").extract()[0]
        item['brand'] = product_details.css("h2 > a::text").extract()[0]
        item['price'] = product_details.css("div.price > span::text").extract()[0]
        item['images'] = response.css("div#large-image img::attr('src')").extract()
        item['note'] = response.css("ul#editors-notes-content > li > div").extract()[0]
        item['link'] = response.request.url
        yield item

        for href in response.css("div#alternative-colors a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)