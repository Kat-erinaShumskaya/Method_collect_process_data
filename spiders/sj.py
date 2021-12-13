import scrapy
from scrapy.http import  HtmlResponse
from jobparser.items import JobparserItem


class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response):
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@target="_blank"]/@href').getall()
        # /vakansii
        for link in links:
            if '/vakansii/' in link:
                yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        salary = response.xpath("//h1/following-sibling::span/span//text()").getall()
        # salary = response.xpath('//span[@class="_2Wp8I _1e6dO _1XzYb _3Jn4o"]//text()').getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item
