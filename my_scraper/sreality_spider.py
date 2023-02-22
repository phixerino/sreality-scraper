import scrapy
from scrapy.item import Item, Field
from scrapy import Request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class UrlItem(Item):
    title = Field()
    url = Field()


class SrealitySpider(scrapy.Spider):
    name = 'sreality_spider'
    start_urls = ['https://www.sreality.cz/hledani/prodej/byty']

    def __init__(self, max_count=500, *args, **kwargs):
        super(SrealitySpider, self).__init__(*args, **kwargs)
        self.max_count = max_count
        self.count = 0

    def parse(self, response):
        go_next = True
        url_items = []
        for image_hyperlink in response.xpath('//div[@class="dir-property-list"]').xpath('.//a'):
            img_url = image_hyperlink.xpath('img[@src and not(@ng-src)]/@src').get()
            if img_url:
                url_item = UrlItem()
                url_item['title'] = response.urljoin(image_hyperlink.xpath('@href').get())
                url_item['url'] = response.urljoin(img_url)
                url_items.append(url_item)
                self.count += 1
                if self.count >= self.max_count:
                    go_next = False
                    break

        if go_next:
            next_page_url = response.urljoin(response.xpath('//a[@class="btn-paging-pn icof icon-arr-right paging-next"]/@href').get())
            yield Request(next_page_url, callback=self.parse)

        for url_item in url_items:
            yield url_item

