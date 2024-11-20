import scrapy
import json
import requests
import os

class QuotesSpider(scrapy.Spider):
    name = "daswerk"

    # Retrieve Telegram bot credentials from environment variables
    telegram_token = os.getenv('7632336346:AAFFHy1tYpwGu2N_em62QbDvvD5HThHMbaQ')  # Telegram bot token from environment variables
    chat_id = os.getenv('-4533482229')  # Telegram chat ID from environment variables

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

        # Combine <a>, <h2>, and <li> elements into a structured dictionary
        combined_links_and_headings = []

        # Zip together <a>, <h2>, and <li> to form a list of dicts
        for a, h, li in zip(a_elements, h2_elements, li_elements):
            combined_links_and_headings.append({
                'link': a,
                'heading': h,
                'text': li
            })

        # If there are more li_elements than links and headings, append the extra li_elements
        remaining_li_elements = li_elements[len(a_elements):]
        for li in remaining_li_elements:
            combined_links_and_headings.append({
                'link': None,  # No link for these elements
                'heading': None,  # No heading for these elements
                'text': li
            })

        # Save the structured data to a JSON file
        with open('data2.json', 'w') as f:
            json.dump(combined_links_and_headings, f)

        # Yield the final structured data (optional)
        yield {
            'link_heading_pairs': combined_links_and_headings,
        }

    def close(self, reason):
        """Once the spider finishes, read the JSON file and send its content to Telegram"""
        with open('data2.json', 'r') as f:
            data = json.load(f)

        # Format the message to send to Telegram
        message = self.format_message(data)

        # Send the formatted message to Telegram
        self.send_telegram_message(message)

    def format_message(self, data):
        """Format the message to be sent to Telegram"""
        message = "Here are the latest items from the website:\n\n"
        for item in data:
            if item['heading'] and item['link']:
                message += f"📎 *{item['heading']}*\n"
                message += f"🔗 Link: {item['link']}\n"
            elif item['text']:
                message += f"📄 {item['text']}\n"  # For li elements without a link or heading
            message += "\n"

        return message

    def send_telegram_message(self, message):
        """Send a message to a Telegram chat using the Bot API"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown',  # Use Markdown for formatting
        }

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                self.log(f"Message sent to Telegram: {message}")
            else:
                self.log(f"Failed to send message: {response.status_code}")
        except Exception as e:
            self.log(f"Error sending message: {e}")
