import requests
import sqlite3
import json
from datetime import datetime

DB_FILE = 'defillama_data.db'
# Initialize and connect to SQLite database for historical data
def init_historical_db():
    conn = sqlite3.connect(DB_FILE)
    return conn

# Query the defillama_data.db database for chains with TVL higher than 50K
def query_high_tvl_chains():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM chain_data WHERE tvl > 50000")
    chains = cursor.fetchall()
    conn.close()
    # Use only the first word of the name and exclude None values
    return [chain[0].split()[0] for chain in chains if chain[0]]

# Fetch historical TVL data for a chain
def fetch_historical_tvl(chain_name):
    url = f"https://api.llama.fi/v2/historicalChainTvl/{chain_name}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list) and all(isinstance(item, dict) and 'date' in item and 'tvl' in item for item in data):
                return data
            else:
                raise ValueError(f"Data format is not as expected for {chain_name}: {data}")
        except ValueError as ve:
            print(ve)
            return []
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for {chain_name}")
            return []
    else:
        print(f"Failed to fetch historical TVL data for {chain_name} with status code {response.status_code}")
        return []

# Convert UNIX timestamp to standard date format
def convert_unix_to_standard_date(unix_timestamp):
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d')

# Create a table for a chain in the historical database
def create_table_for_chain(conn, chain_name):
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {chain_name} (
            date TEXT PRIMARY KEY,
            tvl REAL
        )
    ''')
    conn.commit()

# Insert historical data into the chain's table
def insert_historical_data(conn, chain_name, historical_data):
    cursor = conn.cursor()
    for data in historical_data:
        date = convert_unix_to_standard_date(data['date'])
        tvl = data['tvl']
        # Check for existing record before inserting
        cursor.execute(f'SELECT tvl FROM {chain_name} WHERE date = ?', (date,))
        if not cursor.fetchone():
            cursor.execute(f'INSERT INTO {chain_name} (date, tvl) VALUES (?, ?)', (date, tvl))
    conn.commit()

def main():
    chains = query_high_tvl_chains()
    conn = init_historical_db()

    for chain in chains:
        try:
            historical_data = fetch_historical_tvl(chain)
            create_table_for_chain(conn, chain)
            insert_historical_data(conn, chain, historical_data)
            print(f"Data for {chain} inserted successfully.")
        except Exception as e:
            print(f"An error occurred with {chain}: {e}")

    conn.close()

if __name__ == "__main__":
    main()
