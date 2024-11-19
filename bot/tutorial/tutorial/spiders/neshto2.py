import scrapy
import requests

class QuotesSpider(scrapy.Spider):
    name = "daswerk3"
    telegram_token = '7632336346:AAFFHy1tYpwGu2N_em62QbDvvD5HThHMbaQ'  # Replace with your bot token
    chat_id = '-2481603999'  # Replace with your chat ID

    def start_requests(self):
        urls = [
            "https://www.daswerk.org/programm/",  # Replace with the URL you want to scrape
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
        combined_links_and_headings = [
            {'link': a, 'heading': h} for a, h in zip(a_elements, h2_elements)
        ]

        # Prepare the message to send to Telegram
        message = self.format_message(li_elements, combined_links_and_headings)

        # Send the message to Telegram
        self.send_telegram_message(message)

        # Yield the final structured data (optional)
        yield {
            'text': li_elements,
            'link_heading_pairs': combined_links_and_headings,
        }

    def format_message(self, li_elements, combined_links_and_headings):
        """Format the message to be sent to Telegram"""
        message = "Here are the latest quotes or items from the website:\n\n"
        for item in combined_links_and_headings:
            message += f"📎 *{item['heading']}*\n"  # Heading as bold
            message += f"🔗 Link: {item['link']}\n\n"
        return message

    def send_telegram_message(self, message):
        """Send a message to a Telegram chat using the Bot API"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown'  # Use Markdown for formatting
        }

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                self.log(f"Message sent to Telegram: {message}")
            else:
                self.log(f"Failed to send message: {response.status_code}")
        except Exception as e:
            self.log(f"Error sending message: {e}")
