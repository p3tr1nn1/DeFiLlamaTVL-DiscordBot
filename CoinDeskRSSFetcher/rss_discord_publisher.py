import os
import sqlite3
import requests
import json
import time

# Database path
DATABASE_PATH = 'rss_articles.db'  # Update this path as needed

# Environment variable for Discord webhook
DISCORD_WEBHOOK_URL = os.getenv('COINDESK_DISCORD_WEBHOOK_URL')
MESSAGE_BATCH_SIZE = 10
BATCH_DELAY_SECONDS = 5

def create_news_embed(title, link, description, category):
    """Creates a Discord embed for a news item."""
    return {
        "title": title,
        "description": f"{description}\n\n[Read more...]({link})",
        "color": 5814783,  # You can change the embed color
        "fields": [
            {"name": "Category", "value": category, "inline": False}
        ]
    }

def send_discord_message(embeds):
    """Sends a message to the Discord channel via webhook."""
    data = {"embeds": embeds}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response.status_code == 200

def fetch_unsent_articles_and_notify():
    """Fetch unsent articles, send to Discord, and update the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT title, link, description, category FROM articles WHERE sent_to_discord = 0')
    unsent_articles = cursor.fetchall()

    for index, (title, link, description, category) in enumerate(unsent_articles, start=1):
        embed = create_news_embed(title, link, description, category)
        if send_discord_message([embed]):
            cursor.execute('UPDATE articles SET sent_to_discord = 1 WHERE link = ?', (link,))
            conn.commit()
            print(f"Sent article: {title}")
        else:
            print(f"Failed to send article: {title}")

        if index % MESSAGE_BATCH_SIZE == 0:
            time.sleep(BATCH_DELAY_SECONDS)

    conn.close()

def main():
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL is not set. Please set the COINDESK_DISCORD_WEBHOOK_URL environment variable.")
        return

    fetch_unsent_articles_and_notify()

if __name__ == '__main__':
    main()
