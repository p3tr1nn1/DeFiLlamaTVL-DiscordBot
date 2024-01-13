import feedparser
import sqlite3
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

# Database configuration
DATABASE_PATH = 'central_rss_articles.db'

# RSS Feed URLs
COINDESK_RSS_URL = 'https://www.coindesk.com/arc/outboundfeeds/rss/'
DEFIANT_RSS_URL = 'https://thedefiant.io/feed/'  # Update this with the correct URL
INVESTING_RSS_URL = 'https://www.investing.com/rss/news_301.rss'


def setup_database():
    """Sets up the database for storing articles."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            title TEXT,
            link TEXT PRIMARY KEY,
            description TEXT,
            publication_date TEXT,
            content_url TEXT,
            sent_to_discord BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def format_pub_date(pub_date_str):
    """Formats the publication date to a sortable format."""
    try:
        return datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def fetch_and_store_coindesk_rss_feed(url):
    """Fetches RSS feed and stores articles in the database."""
    feed = feedparser.parse(url)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description = entry.description
        pub_date = format_pub_date(entry.published)
        content_url = entry.get('media_content', [{}])[0].get('url', 'No Image')

        cursor.execute('''
            INSERT OR IGNORE INTO articles (title, link, description, publication_date, content_url, sent_to_discord)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, link, description, pub_date, content_url, False))

    conn.commit()
    conn.close()


def format_defiant_pub_date(pub_date_str):
    """Formats the publication date for The Defiant's feed."""
    try:
        # Convert to datetime object, considering the timezone
        time_tuple = parsedate_tz(pub_date_str)
        dt = datetime.fromtimestamp(mktime_tz(time_tuple))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return 'Unknown'


def fetch_and_store_defiant_rss_feed():
    """Fetches RSS feed from The Defiant and stores articles in the database."""
    rss_url = 'https://thedefiant.io/api/feed'  # Defiant RSS URL
    feed = feedparser.parse(rss_url)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description = entry.description
        pub_date = format_defiant_pub_date(entry.get('published', 'Unknown'))
        thumbnail_url = entry.get('media_thumbnail', [{}])[0].get('url', 'No Image')

        # Check if entry already exists in the articles table
        cursor.execute('SELECT link FROM articles WHERE link = ?', (link,))
        if cursor.fetchone():
            continue  # Skip if entry already exists

        # Insert into the articles table
        cursor.execute('''
            INSERT INTO articles (title, link, description, publication_date, content_url, sent_to_discord)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, link, description, pub_date, thumbnail_url, False))

    conn.commit()
    conn.close()

def fetch_and_store_investing_rss_feed():
    """Fetches RSS feed from Investing and stores articles in the database."""
    feed = feedparser.parse(INVESTING_RSS_URL)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        # Corrected column name from 'pub_date' to 'publication_date'
        publication_date = datetime.strptime(entry.published, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        content_url = entry.enclosures[0].href if entry.enclosures else 'No Image'

        # Corrected INSERT statement to use 'publication_date'
        cursor.execute('''
            INSERT INTO articles (title, link, description, publication_date, content_url, sent_to_discord)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, link, '', publication_date, content_url, False))

    conn.commit()
    conn.close()



def main():
    setup_database()
    fetch_and_store_coindesk_rss_feed(COINDESK_RSS_URL)
    fetch_and_store_defiant_rss_feed()
    fetch_and_store_investing_rss_feed()

if __name__ == '__main__':
    main()
