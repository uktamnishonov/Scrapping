import scrapy
from urllib.parse import urljoin
import datetime


class AxborotSpider(scrapy.Spider):
    name = 'axborot'
    base_url = 'https://yangihayottumani.uz/uzc/news/information-service?child=authority-news&page={}'
    def start_requests(self):
        url = self.base_url.format(1)
        yield scrapy.Request(url, self.parse_url)


    def parse_url(self, response):
        articles = response.css('div.col-md-4.col-sm-6.mt-4')
        domain = 'https://yangihayottumani.uz'
        article_list = []
        if not articles:
            self.log('No more pages with news articles. Stopping the spider.')
            return

        for new in articles:
            absolute_url = urljoin(domain, new.css('a.card-img::attr(href)').extract_first())
            article_list.append(absolute_url)
            yield scrapy.Request(absolute_url, callback=self.parse_item)


        current_page_number = int(response.url.split('=')[-1])
        next_page_number = current_page_number + 1
        next_page_url = self.base_url.format(next_page_number)

        yield scrapy.Request(next_page_url, self.parse_url)

    def parse_item(self, response):
        yield {
            'url': response.url,
            'title': response.css('div.info-top h3::text').extract_first(),
            'text': response.css('div.news-about-text p::text').extract(),
            'creation_date': response.css('div.sotcial span::text').extract_first(),
            'access_date': datetime.datetime.now()
        }
