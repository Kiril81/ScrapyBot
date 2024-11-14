from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://www.daswerk.org/programm/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
         # Extract all <ul> elements
        li_elements = response.css('li::text').getall()

         # Extract all <a> elements
        a_elements = response.xpath('//a/@href').getall()
        # Extract all <h2> elements
        h2_elements = response.css('h2::text').getall()

        # Store all extracted elements in a single dictionary
        yield {
            'text': li_elements,
            'links': a_elements,
            'headings': h2_elements
         }