import scrapy

class QuotesSpider(scrapy.Spider):
    name = "daswerk3"

    def start_requests(self):
        urls = [
            "https://www.daswerk.org/programm/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extract all <li> elements' text
        li_elements = response.css('li::text').getall()

        # Extract all <a> elements' href attributes
        a_elements = response.xpath('//a/@href').getall()

        # Extract all <h2> elements' text
        h2_elements = response.css('h2::text').getall()

        # Ensure that the length of a_elements and h2_elements are the same before pairing them
        # If they are not, you need to decide how to handle this situation (e.g., truncating to the shortest list)
        combined_links_and_headings = [
            {'link': a, 'heading': h} for a, h in zip(a_elements, h2_elements)
        ]

        # Yield the final structured data
        yield {
            'text': li_elements,
            'link_heading_pairs': combined_links_and_headings,  # Pairs of links and headings
        }
