import sqlite3
import json

DATABASE_PATH = 'central_rss_articles.db'
JSON_OUTPUT_PATH = 'discord_queue_data.json'

def fetch_data_from_db():
    """Fetches data from the discord_queue table in the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM discord_queue')
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    conn.close()
    return [dict(zip(columns, row)) for row in data]

def write_json_file(data, file_path):
    """Writes the provided data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    data = fetch_data_from_db()
    write_json_file(data, JSON_OUTPUT_PATH)
    print(f"JSON file generated: {JSON_OUTPUT_PATH}")

if __name__ == '__main__':
    main()
