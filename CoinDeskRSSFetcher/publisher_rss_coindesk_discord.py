import os
import sqlite3
import requests
import json
import time
from datetime import datetime
from email.utils import parsedate_to_datetime  # for parsing RFC 2822 dates

# Database path
DATABASE_PATH = 'rss_articles.db'  # Update this path as needed

# Environment variable for Discord webhook
DISCORD_WEBHOOK_URL = os.getenv('COINDESK_DISCORD_WEBHOOK_URL')
MESSAGE_BATCH_SIZE = 10
BATCH_DELAY_SECONDS = 5

def format_pub_date(pub_date_str):
    """Formats the publication date to a more readable format."""
    try:
        pub_date = parsedate_to_datetime(pub_date_str)
        return pub_date.strftime('%B %d, %Y')
    except Exception:
        return pub_date_str  # Return the original string if parsing fails

def create_news_embed(title, link, description, category, content_url, pub_date):
    """Creates a Discord embed for a news item."""
    formatted_date = format_pub_date(pub_date)
    embed = {
        "title": title,
        "description": f"{description}\n\nPublished on: {formatted_date}\n[Read more...]({link})",
        "color": 5814783,  # You can change the embed color
        "fields": [
            {"name": "Category", "value": category, "inline": False}
        ]
    }
    if content_url:
        embed["image"] = {"url": content_url}
    return embed

def send_discord_message(embeds):
    """Sends a message to the Discord channel via webhook."""
    data = {"embeds": embeds}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response.status_code == 200

def fetch_unsent_articles_and_notify():
    """Fetch unsent articles, sort by publication date, send to Discord, and update the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT title, link, description, category, content_url, publication_date FROM articles WHERE sent_to_discord = 0')
    unsent_articles = cursor.fetchall()

    # Sort articles by publication date
    unsent_articles.sort(key=lambda x: parsedate_to_datetime(x[5]))

    for index, (title, link, description, category, content_url, pub_date) in enumerate(unsent_articles, start=1):
        embed = create_news_embed(title, link, description, category, content_url, pub_date)
        if send_discord_message([embed]):
            cursor.execute('UPDATE articles SET sent_to_discord = 1 WHERE link = ?', (link,))
            conn.commit()
            print(f"Sent article: {title}")
        else:
            print(f"News '{title}' was probably already sent or an error occurred.")

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
