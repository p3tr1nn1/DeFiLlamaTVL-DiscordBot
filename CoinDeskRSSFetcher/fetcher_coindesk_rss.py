import sqlite3
import feedparser

# Database path as a variable
DATABASE_PATH = 'rss_articles.db'  # Update this path as needed

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
            creator TEXT,
            category TEXT,
            content_url TEXT,
            content_type TEXT,
            content_height INTEGER,
            content_width INTEGER,
            sent_to_discord BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Parse RSS Feed
def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description = entry.description
        pub_date = entry.get('published', 'Unknown')
        creator = entry.get('dc_creator', 'Unknown')
        category = ', '.join(cat['term'] for cat in entry.get('tags', []))
        content_url = entry.get('media_content', [{}])[0].get('url', 'Unknown')
        content_type = entry.get('media_content', [{}])[0].get('type', 'Unknown')
        content_height = entry.get('media_content', [{}])[0].get('height', None)
        content_width = entry.get('media_content', [{}])[0].get('width', None)

        # Check if entry already exists
        cursor.execute('SELECT link FROM articles WHERE link = ?', (link,))
        if cursor.fetchone():
            conn.close()
            print("No new articles. Exiting.")
            return  # Exit if entry already exists

        # Insert into the database
        cursor.execute('''
            INSERT INTO articles (title, link, description, publication_date, creator, category, content_url, content_type, content_height, content_width, sent_to_discord)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, link, description, pub_date, creator, category, content_url, content_type, content_height, content_width, False))

    conn.commit()
    conn.close()

# Main function
def main():
    rss_url = 'https://www.coindesk.com/arc/outboundfeeds/rss/'
    setup_database()
    fetch_rss_feed(rss_url)

if __name__ == '__main__':
    main()