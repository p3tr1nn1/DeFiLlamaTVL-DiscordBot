import os
import sqlite3
import requests
import time
from email.utils import parsedate_to_datetime

# Update with your database path
DATABASE_PATH = 'central_rss_articles.db'
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
MESSAGE_BATCH_SIZE = 10
BATCH_DELAY_SECONDS = 5

def format_pub_date(pub_date_str):
    try:
        pub_date = parsedate_to_datetime(pub_date_str)
        return pub_date.strftime('%B %d, %Y')
    except Exception:
        return pub_date_str

def create_news_embed(title, link, description, content_url, pub_date):
    formatted_date = format_pub_date(pub_date)
    embed = {
        "title": title,
        "description": f"{description}\n\nPublished on: {formatted_date}\n[Read more...]({link})",
        "color": 5814783
    }
    if content_url:
        embed["image"] = {"url": content_url}
    return embed

def send_discord_message(embeds):
    data = {"embeds": embeds}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response.status_code == 200

def fetch_unsent_articles_and_notify():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT title, link, description, content_url, publication_date FROM discord_queue ORDER BY publication_date')
    unsent_articles = cursor.fetchall()

    for index, (title, link, description, content_url, pub_date) in enumerate(unsent_articles, start=1):
        embed = create_news_embed(title, link, description, content_url, pub_date)
        if send_discord_message([embed]):
            cursor.execute('DELETE FROM discord_queue WHERE link = ?', (link,))
            conn.commit()
            print(f"Sent article: {title}")
        else:
            print(f"Failed to send article: {title}")

        if index % MESSAGE_BATCH_SIZE == 0:
            time.sleep(BATCH_DELAY_SECONDS)

    conn.close()

def main():
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL is not set. Please set the DISCORD_WEBHOOK_URL environment variable.")
        return

    fetch_unsent_articles_and_notify()

if __name__ == '__main__':
    main()
