import sqlite3
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

# Central database path
DATABASE_PATH = 'central_rss_articles.db'

def setup_discord_queue_table():
    """ Sets up the discord_queue table """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discord_queue (
            title TEXT,
            link TEXT PRIMARY KEY,
            description TEXT,
            publication_date TEXT,
            category TEXT,
            content_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def process_coindesk_articles():
    """ Processes articles from coindesk_articles and updates sent_to_discord """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Select articles that have not been sent to Discord
    cursor.execute('SELECT title, link, description, publication_date, category, content_url FROM coindesk_articles WHERE sent_to_discord = 0')
    articles = cursor.fetchall()

    # Process each article
    for article in articles:
        title, link, description, publication_date, category, content_url = article

        # Insert article into discord_queue
        cursor.execute('''
            INSERT INTO discord_queue (title, link, description, publication_date, category, content_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, link, description, publication_date, category, content_url))

        # Update sent_to_discord in coindesk_articles
        cursor.execute('''
            UPDATE coindesk_articles SET sent_to_discord = 1 WHERE link = ?
        ''', (link,))

    conn.commit()
    conn.close()

def process_defiant_articles():
    """ Processes articles from defiant_articles and updates sent_to_discord """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Select articles that have not been sent to Discord
    cursor.execute('SELECT title, link, description, publication_date, thumbnail_url FROM defiant_articles WHERE sent_to_discord = 0')
    articles = cursor.fetchall()

    # Process each article
    for article in articles:
        title, link, description, publication_date, thumbnail_url = article

        # Insert article into discord_queue (using thumbnail_url as content_url)
        cursor.execute('''
            INSERT INTO discord_queue (title, link, description, publication_date, content_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, link, description, publication_date, thumbnail_url))

        # Update sent_to_discord in defiant_articles
        cursor.execute('''
            UPDATE defiant_articles SET sent_to_discord = 1 WHERE link = ?
        ''', (link,))

    conn.commit()
    conn.close()

def process_investing_articles():
    """ Processes articles from investing_articles and updates sent_to_discord """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Adjust the SELECT query to match the actual columns in the investing_articles table
    cursor.execute('SELECT title, link, pub_date AS publication_date, content_url FROM investing_articles WHERE sent_to_discord = 0')
    articles = cursor.fetchall()

    # Process each article
    for article in articles:
        title, link, publication_date, content_url = article

        # Insert article into discord_queue
        # Omitting the description as it's not available in the investing_articles table
        cursor.execute('''
            INSERT INTO discord_queue (title, link, publication_date, content_url)
            VALUES (?, ?, ?, ?)
        ''', (title, link, publication_date, content_url))

        # Update sent_to_discord in investing_articles
        cursor.execute('''
            UPDATE investing_articles SET sent_to_discord = 1 WHERE link = ?
        ''', (link,))

    conn.commit()
    conn.close()

def standardize_date(date_str):
    """Converts various date formats to a standardized format (YYYY-MM-DD HH:MM:SS)."""
    try:
        # Try parsing as RFC 2822 format (e.g., Thu, 11 Jan 2024 15:32:46 +0000)
        time_tuple = parsedate_tz(date_str)
        if time_tuple:
            dt = datetime.fromtimestamp(mktime_tz(time_tuple))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            raise ValueError("Invalid date format")
    except Exception as e:
        # If parsing fails, assume it's already in the desired format
        return date_str

def update_publication_dates():
    """Updates the publication dates in the discord_queue table to a standard format."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Select all rows from discord_queue
    cursor.execute('SELECT link, publication_date FROM discord_queue')
    rows = cursor.fetchall()

    # Update each row with the standardized date
    for link, publication_date in rows:
        standardized_date = standardize_date(publication_date)
        cursor.execute('''
            UPDATE discord_queue SET publication_date = ? WHERE link = ?
        ''', (standardized_date, link))

    conn.commit()
    conn.close()


def delete_entries_without_description():
    """Deletes entries from the discord_queue table where the description is NULL or empty."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # SQL command to delete rows where description is NULL or empty
    cursor.execute('DELETE FROM discord_queue WHERE description IS NULL OR description = ""')

    conn.commit()
    conn.close()


def main():
    setup_discord_queue_table()
    process_coindesk_articles()
    process_defiant_articles()
    process_investing_articles()
    delete_entries_without_description()
    update_publication_dates()

if __name__ == '__main__':
    main()
