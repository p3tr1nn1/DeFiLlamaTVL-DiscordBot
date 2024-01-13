import os
import sqlite3
import requests
import json
import time

# Database path
DATABASE_PATH = 'defiant_articles.db'  # Update this path as needed

# Environment variable for Discord webhook
DISCORD_WEBHOOK_URL = os.getenv('COINDESK_DISCORD_WEBHOOK_URL')
MESSAGE_BATCH_SIZE = 10
BATCH_DELAY_SECONDS = 5

def create_news_embed(title, link, description, thumbnail_url, pub_date):
    """Creates a Discord embed for a news item."""
    embed = {
        "title": title,
        "description": f"{description}\n\nPublished on: {pub_date}\n[Read more...]({link})",
        "color": 5814783,
    }
    if thumbnail_url:
        embed["image"] = {"url": thumbnail_url}
    return embed

def send_discord_message(embeds):
    """Sends a message to the Discord channel via webhook."""
    data = {"embeds": embeds}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error sending Discord message: {e}")
        return False

def update_article_sent_status(cursor, link):
    """Update the sent_to_discord status for an article."""
    try:
        cursor.execute('UPDATE articles SET sent_to_discord = 1 WHERE link = ?', (link,))
        return True
    except sqlite3.Error as e:
        print(f"Error updating sent status for link {link}: {e}")
        return False

def fetch_unsent_articles_and_notify():
    """Fetch unsent articles, sort by publication date, send to Discord, and update the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute('BEGIN')
        cursor.execute('SELECT title, link, description, thumbnail_url, publication_date FROM articles WHERE sent_to_discord = 0 ORDER BY publication_date ASC')
        unsent_articles = cursor.fetchall()

        for article in unsent_articles:
            embed = create_news_embed(article['title'], article['link'], article['description'], article['thumbnail_url'], article['publication_date'])
            if send_discord_message([embed]):
                if update_article_sent_status(cursor, article['link']):
                    print(f"Sent article and updated database: {article['title']}")
                else:
                    print(f"Failed to update database for article: {article['title']}")
            else:
                print(f"Error sending '{article['title']}' to Discord. Skipping update.")

            if (unsent_articles.index(article) + 1) % MESSAGE_BATCH_SIZE == 0:
                time.sleep(BATCH_DELAY_SECONDS)

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL is not set. Please set the COINDESK_DISCORD_WEBHOOK_URL environment variable.")
        return

    fetch_unsent_articles_and_notify()

if __name__ == '__main__':
    main()
