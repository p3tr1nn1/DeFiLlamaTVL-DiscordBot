import requests
import sqlite3
from datetime import datetime

# Initialize and connect to SQLite database
def init_db():
    conn = sqlite3.connect('defillama_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_growth_chains (
            chain_name TEXT,
            percentage_increase_30d REAL,
            percentage_increase_7d REAL,
            percentage_increase_1d REAL,
            current_tvl REAL,
            date_recorded DATETIME
        )
    ''')
    conn.commit()
    return conn

# Fetch historical TVL data for a chain
def fetch_historical_tvl(chain_name):
    url = f"https://api.llama.fi/v2/historicalChainTvl/{chain_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch historical TVL data for {chain_name}")

# Query database for chains with TVL higher than 5 million
def query_chains(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT gecko_id FROM chain_data WHERE tvl > 5000000")
    chains = cursor.fetchall()
    return [chain[0] for chain in chains]

# Insert data into the high_growth_chains table
def insert_high_growth_data(conn, chain_name, increase_30d, increase_7d, increase_1d, current_tvl):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO high_growth_chains (chain_name, percentage_increase_30d, percentage_increase_7d, percentage_increase_1d, current_tvl, date_recorded)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (chain_name, increase_30d, increase_7d, increase_1d, current_tvl, datetime.now(),))
    conn.commit()

# Calculate percentage increase
def calculate_percentage_increase(current_tvl, previous_tvl):
    return ((current_tvl - previous_tvl) / previous_tvl) * 100 if previous_tvl else 0

# Compare current TVL with TVL from 1 day, 7 days, and 30 days ago
def compare_tvl(conn, chain_name):
    try:
        historical_data = fetch_historical_tvl(chain_name)
        if len(historical_data) < 30:
            return

        current_tvl = historical_data[-1]['tvl']
        tvl_1_day_ago = historical_data[-2]['tvl'] if len(historical_data) >= 2 else 0
        tvl_7_days_ago = historical_data[-8]['tvl'] if len(historical_data) >= 8 else 0
        tvl_30_days_ago = historical_data[-30]['tvl']

        increase_1d = calculate_percentage_increase(current_tvl, tvl_1_day_ago)
        increase_7d = calculate_percentage_increase(current_tvl, tvl_7_days_ago)
        increase_30d = calculate_percentage_increase(current_tvl, tvl_30_days_ago)

        if increase_30d > 30:
            insert_high_growth_data(conn, chain_name, increase_30d, increase_7d, increase_1d, current_tvl)
    except Exception as e:
        print(f"An error occurred while processing {chain_name}: {e}")

# Print high growth chains data
def print_high_growth_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT chain_name, percentage_increase_30d FROM high_growth_chains")
    for row in cursor.fetchall():
        print(f"{row[0]} TVL increased by {row[1]:.2f}% over the last 30 days.")

def main():
    conn = init_db()
    chains = query_chains(conn)
    for chain in chains:
        compare_tvl(conn, chain)
    print_high_growth_data(conn)
    conn.close()

if __name__ == "__main__":
    main()
