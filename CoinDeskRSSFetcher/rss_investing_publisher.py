import os
import sqlite3
import requests
import json
import time
import time
from datetime import datetime
# Database path
DATABASE_PATH = 'investing_articles.db'  # Update this path as needed

# Environment variable for Discord webhook
DISCORD_WEBHOOK_URL = os.getenv('COINDESK_DISCORD_WEBHOOK_URL')
MESSAGE_BATCH_SIZE = 10
BATCH_DELAY_SECONDS = 5

def format_pub_date(pub_date_str):
    """Formats the publication date to a more readable format."""
    try:
        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d %H:%M:%S')
        return pub_date.strftime('%B %d, %Y')
    except ValueError:
        return pub_date_str

def create_news_embed(title, link, author, pub_date, content_url):
    """Creates a Discord embed for a news item."""
    formatted_date = format_pub_date(pub_date)
    embed = {
        "title": title,
        "description": f"By {author}\nPublished on: {formatted_date}\n[Read more...]({link})",
        "color": 5814783
    }
    if content_url and content_url != "No Image":
        embed["image"] = {"url": content_url}
    return embed

def send_discord_message(embeds):
    """Sends a message to the Discord channel via webhook."""
    data = {"embeds": embeds}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response.status_code == 200

def fetch_unsent_articles_and_notify():
    """Fetch unsent articles, send to Discord, and update the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT title, link, author, pub_date, content_url FROM articles WHERE sent_to_discord = 0 ORDER BY pub_date ASC')
    unsent_articles = cursor.fetchall()

    for index, (title, link, author, pub_date, content_url) in enumerate(unsent_articles, start=1):
        embed = create_news_embed(title, link, author, pub_date, content_url)
        if send_discord_message([embed]):
            cursor.execute('UPDATE articles SET sent_to_discord = 1 WHERE link = ?', (link,))
            conn.commit()
            print(f"Sent article: {title}")
        else:
            print(f"Failed to send article '{title}'. It might have already been sent.")

        if index % MESSAGE_BATCH_SIZE == 0:
            time.sleep(BATCH_DELAY_SECONDS)

    conn.close()

def main():
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL is not set. Please set the INVESTING_DISCORD_WEBHOOK_URL environment variable.")
        return

    fetch_unsent_articles_and_notify()

if __name__ == '__main__':
    main()
