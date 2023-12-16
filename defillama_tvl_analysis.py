import requests
import sqlite3
from datetime import datetime, timedelta
import json

# Query the defillama_data.db database for chains with TVL higher than 5 million
def query_high_tvl_chains():
    conn = sqlite3.connect('defillama_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM chain_data WHERE tvl > 5000000")
    chains = cursor.fetchall()
    conn.close()
    return [chain[0] for chain in chains]

# Calculate percentage increase
def calculate_percentage_increase(current_tvl, previous_tvl):
    return ((current_tvl - previous_tvl) / previous_tvl) * 100 if previous_tvl else 0

# Fetch historical TVL data and calculate differences
def analyze_tvl(chain_name):
    # Sanitize the chain_name to create a valid SQL table name
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
    formatted_current_tvl = "{:,}".format(current_tvl)  # Format TVL with commas
    tvl_30_days_ago = data[30][1]
    increase_30d = calculate_percentage_increase(current_tvl, tvl_30_days_ago)

    if increase_30d > 20:
        tvl_1_day_ago = data[1][1]
        tvl_7_days_ago = data[7][1]
        increase_1d = calculate_percentage_increase(current_tvl, tvl_1_day_ago)
        increase_7d = calculate_percentage_increase(current_tvl, tvl_7_days_ago)
        message = f"{chain_name} TVL increased by {increase_30d:.2f}% over the last 30 days, {increase_7d:.2f}% over the last 7 days, and {increase_1d:.2f}% over the last day."
        return {"chain": chain_name, "message": message, "current_tvl": formatted_current_tvl}

def main():
    chains = query_high_tvl_chains()
    analysis_results = []

    for chain in chains:
        result = analyze_tvl(chain)
        if result:
            analysis_results.append(result)

    # Sort the results by current TVL in descending order
    sorted_results = sorted(analysis_results, key=lambda x: x['current_tvl'], reverse=True)

    # Write sorted analysis results to a JSON file
    with open('tvl_analysis_results.json', 'w') as file:
        json.dump(sorted_results, file, indent=4)

    # Print messages in a formatted manner
    for result in sorted_results:
        print(result["message"])

if __name__ == "__main__":
    main()
