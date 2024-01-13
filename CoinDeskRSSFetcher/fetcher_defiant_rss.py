import sqlite3
import feedparser
from datetime import datetime
from email.utils import parsedate_to_datetime

# Database path
DATABASE_PATH = 'defiant_articles.db'  # Update this path as needed

# Database setup
def setup_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            title TEXT,
            link TEXT PRIMARY KEY,
            description TEXT,
            publication_date TEXT,
            thumbnail_url TEXT,
            sent_to_discord BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Format publication date
def format_pub_date(pub_date_str):
    try:
        pub_date = parsedate_to_datetime(pub_date_str)
        return pub_date.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return 'Unknown'  # Return 'Unknown' if parsing fails

# Parse RSS Feed
def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description = entry.description
        pub_date = format_pub_date(entry.get('published', 'Unknown'))
        thumbnail_url = entry.get('media_thumbnail', [{}])[0].get('url', 'Unknown')

        # Check if entry already exists
        cursor.execute('SELECT link FROM articles WHERE link = ?', (link,))
        if cursor.fetchone():
            continue  # Skip if entry already exists

        # Insert into the database
        cursor.execute('''
            INSERT INTO articles (title, link, description, publication_date, thumbnail_url, sent_to_discord)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, link, description, pub_date, thumbnail_url, False))

    conn.commit()
    conn.close()

# Main function
def main():
    rss_url = 'https://thedefiant.io/api/feed'
    setup_database()
    fetch_rss_feed(rss_url)

if __name__ == '__main__':
    main()
