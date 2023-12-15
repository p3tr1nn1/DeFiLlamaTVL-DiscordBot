# File: defillama_data_fetcher.py
import requests
import sqlite3
from datetime import datetime, timedelta

def initialize_database():
    conn = sqlite3.connect('defillama_tvl.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chain_tvl
                 (chain_name TEXT, current_tvl REAL, date INTEGER, historical_tvl REAL)''')
    conn.commit()
    return conn

def fetch_current_tvl():
    url = "https://api.llama.fi/v2/chains"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def fetch_historical_tvl(chain_name):
    url = f"https://api.llama.fi/v2/historicalChainTvl/{chain_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def store_chain_data(conn, chain, historical_data, thirty_days_ago):
    c = conn.cursor()
    for data in historical_data:
        if data['date'] >= thirty_days_ago:
            # Check if data for the same chain and date already exists in the database
            c.execute('SELECT COUNT(*) FROM chain_tvl WHERE chain_name = ? AND date = ?',
                      (chain['name'], data['date']))
            count = c.fetchone()[0]
            if count == 0:
                # Insert the data only if it's not a duplicate
                c.execute('INSERT INTO chain_tvl VALUES (?, ?, ?, ?)',
                          (chain['name'], chain['tvl'], data['date'], data['tvl']))

    conn.commit()


def fetch_and_store_chain_data():
    conn = initialize_database()
    chains = fetch_current_tvl()
    thirty_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())

    for chain in chains:
        if chain['tvl'] > 10000000:  # TVL greater than 10 million
            print(f"Fetching historical data for chain: {chain['name']}")
            historical_data = fetch_historical_tvl(chain['gecko_id'])
            store_chain_data(conn, chain, historical_data, thirty_days_ago)

    conn.commit()
    conn.close()
    print("Data fetching and storage complete.")
