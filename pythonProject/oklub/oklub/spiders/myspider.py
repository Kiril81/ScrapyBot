import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = [
        'https://o-klub.at/events/'  # Assuming this is the target site
    ]

    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'oklub.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
                'indent': 4,  # Better readable
            },
        },
    }

    def parse(self, response):
        # XPath to extract day and month
        days = response.xpath('//div[@id="day"]/div[@class="elementor-widget-container"]/text()').getall()
        months = response.xpath('//div[@id="month"]/div[@class="elementor-widget-container"]/text()').getall()

        self.log(f"Extracted days: {days}")
        self.log(f"Extracted months: {months}")

        # XPath to extract event name
        event_names = response.xpath('//div[@id="event_name"]//h3/text()').getall()

        self.log(f"Extracted event names: {event_names}")

        # XPath to extract event links
        event_links = response.xpath('//a[contains(@class, "jet-engine-listing-overlay-link")]/@href').getall()

        self.log(f"Extracted event links: {event_links}")

        # Ensure the lists are of the same length
        if len(days) != len(months) or len(days) != len(event_names) or len(days) != len(event_links):
            self.log("Warning: The number of days, months, event names, and links do not match!")

        events = []
        for day, month, event_name, event_link in zip(days, months, event_names, event_links):
            # Append event with day, month, event name, and link
            events.append({
                'day': day.strip(),
                'month': month.strip(),
                'event_name': event_name.strip(),
                'link': event_link.strip(),
            })

        # Yield the events
        yield {
            'events': events
        }
