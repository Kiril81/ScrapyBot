import scrapy
import requests
from scrapy.utils.project import get_project_settings

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.daswerk.org/programm/']

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.telegram_token = '7632336346:AAFFHy1tYpwGu2N_em62QbDvvD5HThHMbaQ'
        self.chat_id = '<your_chat_id>'

    def parse(self, response):
        # Example of scraping some data
        title = response.xpath('//title/text()').get()

        # Send the data to Telegram
        self.send_telegram_message(f"Scraped data: {title}")

    def send_telegram_message(self, message):
        """Send a message to a Telegram chat."""
        url = f'https://api.telegram.org/bot{self.telegram_token}/sendMessage'
        payload = {
            'chat_id': self.chat_id,
            'text': message
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                self.log(f"Message sent to Telegram: {message}")
            else:
                self.log(f"Failed to send message: {response.status_code}")
        except Exception as e:
            self.log(f"Error sending message: {e}")