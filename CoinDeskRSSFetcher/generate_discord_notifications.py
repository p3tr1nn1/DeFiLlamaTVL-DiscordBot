import requests
import json
import time
import os
import random

# Environment variable for Discord webhook
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
JSON_INPUT_PATH = 'unsent_to_discord.json'
MESSAGE_BATCH_SIZE = 10
BATCH_DELAY_SECONDS = 5

RETRY_DELAY_SECONDS = 5
MAX_RETRIES = 3  # Maximum number of retries for a failed message

def create_news_embed(article):
    """Creates a Discord embed for a news item with a random color."""
    embed = {
        "title": article['title'],
        "description": f"{article['description']}\n\nPublished on: {article['publication_date']}\n[Read more...]({article['link']})",
        "color": random.randint(0, 0xFFFFFF)  # Random color
    }
    if article.get('content_url') and article['content_url'] != "No Image":
        embed["image"] = {"url": article['content_url']}
    return embed

def send_discord_message(embeds):
    """Sends a message to the Discord channel via webhook with error handling and retry mechanism."""
    data = {"embeds": embeds}
    attempts = 0

    while attempts < MAX_RETRIES:
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=data)
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - Attempt {attempts + 1} of {MAX_RETRIES}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err} - Attempt {attempts + 1} of {MAX_RETRIES}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err} - Attempt {attempts + 1} of {MAX_RETRIES}")
        except requests.exceptions.RequestException as req_err:
            print(f"Error sending request: {req_err} - Attempt {attempts + 1} of {MAX_RETRIES}")

        attempts += 1
        if attempts < MAX_RETRIES:
            time.sleep(RETRY_DELAY_SECONDS)

    return False

def send_messages_from_json():
    """Sends messages to Discord from JSON file."""
    try:
        with open(JSON_INPUT_PATH, 'r') as file:
            articles = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {JSON_INPUT_PATH}")
        return

    for index, article in enumerate(articles, start=1):
        embed = create_news_embed(article)
        if send_discord_message([embed]):
            print(f"Sent article: {article['title']}")
        else:
            print(f"Failed to send article: {article['title']}")

        if index % MESSAGE_BATCH_SIZE == 0:
            time.sleep(BATCH_DELAY_SECONDS)
def clear_json_file():
    """Clears the contents of the JSON file."""
    with open(JSON_INPUT_PATH, 'w') as file:
        json.dump([], file)  # Write an empty list to the file

def main():
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL is not set. Please set the DISCORD_WEBHOOK_URL environment variable.")
        return

    send_messages_from_json()
    clear_json_file()

if __name__ == '__main__':
    main()
