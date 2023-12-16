import requests
import sqlite3
from datetime import datetime

# API endpoint for fetching protocol data
API_ENDPOINT = "https://api.llama.fi/protocols"

# Initialize and connect to SQLite database for protocol data
def init_protocol_db():
    conn = sqlite3.connect('protocol_data.db')
    print("Connected to the database.")
    return conn

# Fetch protocol data from the API
def fetch_protocol_data():
    try:
        print("Fetching protocol data from the API...")
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        print("Protocol data fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch protocol data: {e}")
        return []

# Create a table for protocols in the database
def create_protocol_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS protocols (
            date TEXT,
            id TEXT PRIMARY KEY,
            name TEXT,
            symbol TEXT,
            url TEXT,
            description TEXT,
            chain TEXT,
            logo TEXT,
            chains TEXT,
            change_1h REAL,
            change_1d REAL,
            change_7d REAL,
            tvl REAL,
            mcap REAL
        )
    ''')
    conn.commit()
    print("Protocol table created.")

# Insert protocol data into the database, overwriting duplicates
def insert_protocol_data(conn, protocol_data):
    cursor = conn.cursor()
    for protocol in protocol_data:
        cursor.execute('''
            INSERT OR REPLACE INTO protocols (
                date, id, name, symbol, url, description, chain, logo, chains,
                change_1h, change_1d, change_7d, tvl, mcap
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), protocol['id'], protocol['name'],
            protocol['symbol'], protocol['url'], protocol['description'], protocol['chain'],
            protocol['logo'], ', '.join(protocol['chains']), protocol['change_1h'],
            protocol['change_1d'], protocol['change_7d'], protocol['tvl'], protocol['mcap']
        ))
        conn.commit()
        print(f"Inserted/Updated data for protocol: {protocol['name']} (ID: {protocol['id']})")

def main():
    conn = init_protocol_db()
    create_protocol_table(conn)
    protocol_data = fetch_protocol_data()
    if protocol_data:
        insert_protocol_data(conn, protocol_data)
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
