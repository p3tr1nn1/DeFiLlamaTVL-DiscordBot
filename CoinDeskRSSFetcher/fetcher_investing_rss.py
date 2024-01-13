import feedparser
import sqlite3
from datetime import datetime

# Central database for all scripts
DATABASE_PATH = 'central_rss_articles.db'

def setup_database():
    """Sets up the database for storing Investing articles."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investing_articles (
            title TEXT,
            link TEXT PRIMARY KEY,
            pub_date TEXT,
            author TEXT,
            content_url TEXT,
            sent_to_discord BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def fetch_and_store_rss_feed(url):
    """Fetches RSS feed from Investing and stores articles in the database."""
    feed = feedparser.parse(url)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        pub_date = datetime.strptime(entry.published, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        author = entry.get('author', 'Unknown')
        content_url = entry.enclosures[0].href if entry.enclosures else 'No Image'

        # Insert article into investing_articles table
        cursor.execute('''
            INSERT OR IGNORE INTO investing_articles (title, link, pub_date, author, content_url, sent_to_discord)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, link, pub_date, author, content_url, False))

    conn.commit()
    conn.close()

def main():
    rss_url = 'https://www.investing.com/rss/news_301.rss'
    setup_database()
    fetch_and_store_rss_feed(rss_url)

if __name__ == '__main__':
    main()
