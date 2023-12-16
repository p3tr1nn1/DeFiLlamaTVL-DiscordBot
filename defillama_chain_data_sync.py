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
            gecko_id TEXT,
            tvl REAL,
            tokenSymbol TEXT,
            cmcId INTEGER,
            name TEXT,
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
        # Skip if chainId or gecko_id is null
        if item['chainId'] is None or item['gecko_id'] is None:
            print(f"Skipping entry with null chainId or gecko_id: {item}")
            continue

        # Check if the entry already exists
        cursor.execute('SELECT * FROM chain_data WHERE gecko_id = ? AND timestamp = ?', (item['gecko_id'], datetime.now().date(),))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO chain_data (gecko_id, tvl, tokenSymbol, cmcId, name, chainId, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (item['gecko_id'], item['tvl'], item['tokenSymbol'], item['cmcId'], item['name'], item['chainId'], datetime.now(),))
            print(f"Inserted data for {item['gecko_id']}.")
    conn.commit()
    print("Data insertion complete.")

#def main():
#    try:
#        data = fetch_data()
#        conn = init_db()
#        insert_data(conn, data)
#        print("Data inserted successfully.")
#    except Exception as e:
#        print(f"An error occurred: {e}")
#    finally:
#        if conn:
#            conn.close()
#if __name__ == "__main__":
#    main()