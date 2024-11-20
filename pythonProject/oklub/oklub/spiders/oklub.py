import json
import requests
from datetime import datetime

# Month conversion dictionary (Abbreviated month names to numeric month)
months = {
    'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
    'JUL': '07', 'AUG': '08', 'SEPT': '09', 'OCT': '10', 'NOV': '11', 'DEZ': '12'
}

# Load JSON file
with open('oklub.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Check if the loaded data is a list and get the first item
if isinstance(data, list) and len(data) > 0:
    first_item = data[0]  # First item in the list

    # Get event data
    events = first_item.get('events', [])

    # Your Telegram bot token
    token = '7632336346:AAFFHy1tYpwGu2N_em62QbDvvD5HThHMbaQ'
    chat_id = 	-4533482229  # Telegram group ID

    # Get today's date in day and month format
    today = datetime.today()
    today_day = today.strftime('%d')
    today_month = today.strftime('%m')

    # Initialize a list to store failed messages
    failed_events = []

    # Process each event
    for event in events:
        day = event.get('day', 'No Day').zfill(2)  # Ensure day is two digits
        month_abbr = event.get('month', 'No Month').upper()  # Month abbreviation
        event_name = event.get('event_name', 'No Event Name')
        link = event.get('link', 'No Link')
        location = event.get('location', 'No location')

        # Convert the abbreviated month to its numeric format
        month = months.get(month_abbr, None)

        # If the month is not found in the dictionary, skip this event
        if not month:
            continue

        # If the event's day and month match today's date, send the message
        if day == today_day and month == today_month:
            # Create a message with day, month, event name, location, and link
            message = f"🎉 Event: {event_name}\n📅 Date: {day}, {month_abbr}\n📌 Location: {location}\n🔗 Link: {link}"

            # Send the message using the Telegram API
            response = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data={
                'chat_id': chat_id,
                'text': message
            })

            # Check if the message was sent successfully
            if response.status_code != 200:
                failed_events.append(event_name)  # Add event name to the list of failed events
            else:
                print(f"Message sent for event: {event_name}")

    # Print failed messages (if any)
    if failed_events:
        print("Failed to send messages for the following events:")
        for failed in failed_events:
            print(failed)
    else:
        print("All messages were successfully sent!")

else:
    print("The JSON structure is not as expected or the list is empty.")