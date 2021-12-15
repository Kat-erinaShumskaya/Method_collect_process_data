import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

# //a[@data-qa-pagination-item='right']/@href
class LeroyruSpider(scrapy.Spider):
    name = 'leroyru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@data-qa-product]/a/@href")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//picture[@slot='pictures']//@srcset")
        yield loader.load_item()
