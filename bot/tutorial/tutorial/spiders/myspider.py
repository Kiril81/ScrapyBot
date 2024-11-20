import scrapy

class QuotesSpider(scrapy.Spider):
    name = "daswerk"

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
        # If they are not, you can decide how to handle the situation (e.g., truncating to the shortest list)
        combined_links_and_headings = []

        # You can also combine the li_elements if their length matches with a_elements and h2_elements
        for a, h, li in zip(a_elements, h2_elements, li_elements):
            combined_links_and_headings.append({
                'link': a,
                'heading': h,
                'text': li  # Add the li text to the dictionary
            })

        # If there are more 'li_elements' than 'a_elements' and 'h2_elements',
        # you can append remaining li_elements with no link and heading
        remaining_li_elements = li_elements[len(a_elements):]
        for li in remaining_li_elements:
            combined_links_and_headings.append({
                'link': None,  # No link
                'heading': None,  # No heading
                'text': li  # Only text from li element
            })

        # Yield the final structured data
        yield {
            'link_heading_pairs': combined_links_and_headings,  # Pairs of links, headings, and li texts
        }
