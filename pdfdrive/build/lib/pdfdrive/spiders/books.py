# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['pdfdrive.com']

    def __init__(self, query):
        self.start_urls = [r'https://www.pdfdrive.com/category/' + str(query)]

    def parse(self, response):


        links = [response.urljoin(link) for link in response.xpath("//*[@class='file-right']/a/@href").extract()]
        for link in links:
            yield Request(link, callback = self.parse_page)
        next_page_url = response.urljoin(response.xpath("//a[@rel='next']/@href").extract_first())
        yield Request(next_page_url)

    def parse_page(self, response):
        ebook_title = response.xpath('//h1[@class="ebook-title"]/text()').extract_first()
        pages, year, size, _ = response.xpath("//div[@class='ebook-file-info']/span[@class='info-green']/text()").extract()
        author =response.xpath('//span[@itemprop="creator"]/text()').extract_first()
        tags = response.xpath('//div[@class="ebook-tags"]/a/text()').extract()
        tags = ','.join(tags)
        download_link = [response.urljoin(link) for link in response.xpath("//a[@id='download-button-link']/@href").extract()][0]

        yield {
        'Title' : ebook_title,
        'Page' : pages,
        'Year' : year,
        'Size' : size,
        'Author' : author,
        'Tags' : tags,
        'Download Link' : download_link,
        }
