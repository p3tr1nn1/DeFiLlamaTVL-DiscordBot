import requests
import sqlite3
from datetime import datetime, timedelta

# Convert UNIX timestamp to human-readable date
def convert_date(unix_timestamp):
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d')

# Fetch historical TVL data for a chain
def fetch_historical_tvl(chain_name):
    print(f"Fetching historical TVL data for {chain_name}...")
    url = f"https://api.llama.fi/v2/historicalChainTvl/{chain_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch historical TVL data for {chain_name}")

# Query database for chains with TVL higher than 5 million
def query_chains():
    conn = sqlite3.connect('defillama_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT gecko_id FROM chain_data WHERE tvl > 5000000")
    chains = cursor.fetchall()
    conn.close()
    return [chain[0] for chain in chains]

# Compare current TVL with TVL from 30 days ago
def compare_tvl(chain_name):
    try:
        historical_data = fetch_historical_tvl(chain_name)
        if len(historical_data) < 30:
            print(f"Not enough historical data for {chain_name}.")
            return

        current_tvl = historical_data[-1]['tvl']
        tvl_30_days_ago = historical_data[-30]['tvl']
        increase = ((current_tvl - tvl_30_days_ago) / tvl_30_days_ago) * 100

        if increase > 25:
            print(f"{chain_name} TVL increased by {increase:.2f}% over the last 30 days.")
            print(f"Current TVL: {current_tvl}, TVL 30 days ago: {tvl_30_days_ago}")
    except Exception as e:
        print(f"An error occurred while processing {chain_name}: {e}")

def main():
    chains = query_chains()
    for chain in chains:
        compare_tvl(chain)

if __name__ == "__main__":
    main()
