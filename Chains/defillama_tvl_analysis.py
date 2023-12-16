import json
import requests
import sqlite3
from datetime import datetime, timedelta

# Query the defillama_data.db database for chains with TVL higher than 5 million
def query_high_tvl_chains():
    conn = sqlite3.connect('defillama_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM chain_data WHERE tvl > 10000000")
    chains = cursor.fetchall()
    conn.close()
    return [chain[0] for chain in chains]

# Calculate percentage increase
def calculate_percentage_increase(current_tvl, previous_tvl):
    return ((current_tvl - previous_tvl) / previous_tvl) * 100 if previous_tvl else 0

# Fetch historical TVL data and calculate differences
def analyze_tvl(chain_name):
    sanitized_chain_name = chain_name.replace(" ", "_").replace("-", "_")
    historical_conn = sqlite3.connect('defillama_historical.db')
    cursor = historical_conn.cursor()

    try:
        cursor.execute(f"SELECT date, tvl FROM '{sanitized_chain_name}' ORDER BY date DESC LIMIT 31")
        data = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"SQL error for chain {chain_name} (sanitized as {sanitized_chain_name}): {e}")
        historical_conn.close()
        return None

    historical_conn.close()

    if len(data) < 31:
        return None  # Not enough data

    current_tvl = data[0][1]
    formatted_current_tvl = "{:,.2f}".format(current_tvl)
    tvl_30_days_ago = data[30][1]
    increase_30d = calculate_percentage_increase(current_tvl, tvl_30_days_ago)

    # Ensure all returned dictionaries have the same structure
    return {
        "chain": chain_name,
        "current_tvl": formatted_current_tvl,
        "increase_30d": increase_30d
    }

def main():
    chains = query_high_tvl_chains()
    analysis_results = []

    for chain in chains:
        result = analyze_tvl(chain)
        if result:
            analysis_results.append(result)

    # Sort the results by 30-day percentage change in descending order
    analysis_results.sort(key=lambda x: x.get("increase_30d", 0), reverse=True)

    # Write analysis results to a JSON file
    with open('tvl_analysis_results.json', 'w') as file:
        json.dump(analysis_results, file, indent=4)

if __name__ == "__main__":
    main()
