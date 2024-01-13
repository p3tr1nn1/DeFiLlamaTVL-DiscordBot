import sqlite3
import json

# Database configuration
DATABASE_PATH = 'central_rss_articles.db'
JSON_OUTPUT_PATH = 'unsent_to_discord.json'

def fetch_unsent_articles():
    """Fetches articles that haven't been sent to Discord, ordered from oldest to newest."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles WHERE sent_to_discord = 0 ORDER BY publication_date ASC')
    unsent_articles = cursor.fetchall()
    conn.close()
    return unsent_articles

def write_to_json_file(data):
    """Writes the provided data to a JSON file."""
    with open(JSON_OUTPUT_PATH, 'w') as file:
        # Convert list of tuples to list of dictionaries for JSON serialization
        articles = [dict(zip(['title', 'link', 'description', 'publication_date', 'content_url', 'sent_to_discord'], article)) for article in data]
        json.dump(articles, file, indent=4)

def update_sent_status():
    """Updates the 'sent_to_discord' status of the articles in the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE articles SET sent_to_discord = 1 WHERE sent_to_discord = 0')
    conn.commit()
    conn.close()

def main():
    unsent_articles = fetch_unsent_articles()
    if unsent_articles:
        write_to_json_file(unsent_articles)
        update_sent_status()
        print(f"{len(unsent_articles)} articles updated and written to {JSON_OUTPUT_PATH}")
    else:
        print("No new articles to send to Discord.")

if __name__ == '__main__':
    main()
