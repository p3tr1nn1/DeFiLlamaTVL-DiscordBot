import requests
import sqlite3
from datetime import datetime

# Fetch data from DeFiLlama API
def fetch_data():
    print("Fetching data from DeFiLlama API...")
    url = "https://api.llama.fi/v2/chains"
    response = requests.get(url)
    if response.status_code == 200:
        print("Data successfully fetched from DeFiLlama API.")
        return response.json()
    else:
        raise Exception("Failed to fetch data from DeFiLlama API")

# Initialize and connect to SQLite database
def init_db():
    print("Initializing database...")
    conn = sqlite3.connect('defillama_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chain_data (
            name TEXT PRIMARY KEY,
            gecko_id TEXT,
            tvl REAL,
            tokenSymbol TEXT,
            cmcId INTEGER,
            chainId INTEGER,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    print("Database initialized.")
    return conn

# Insert data into the database
def insert_data(conn, data):
    print("Inserting data into the database...")
    cursor = conn.cursor()
    for item in data:
        # Insert data with 'name' as the first column
        cursor.execute('''
            INSERT OR IGNORE INTO chain_data (name, gecko_id, tvl, tokenSymbol, cmcId, chainId, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (item.get('name'), item.get('gecko_id'), item.get('tvl'), item.get('tokenSymbol'), item.get('cmcId'), item.get('chainId'), datetime.now(),))
    conn.commit()
    print("Data insertion complete.")

def main():
    try:
        data = fetch_data()
        conn = init_db()
        insert_data(conn, data)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
