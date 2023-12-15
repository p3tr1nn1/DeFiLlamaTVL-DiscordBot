# File: defillama_data_query.py
from datetime import datetime, timedelta

import sqlite3
from defillama_data_fetcher import fetch_and_store_chain_data
from datetime import datetime

def initialize_database():
    conn = sqlite3.connect('defillama_tvl.db')
    return conn

def process_and_display_data():
    # Connect to the database and retrieve data
    db_connection = initialize_database()
    cursor = db_connection.cursor()

    # Get the current date
    current_date = datetime.now()

    # Calculate the date 30 days ago
    thirty_days_ago = current_date - timedelta(days=30)

    # Fetch data from the database
    query = f"SELECT DISTINCT chain_name, current_tvl FROM chain_tvl WHERE current_tvl > 5000000 AND date >= ?"

    cursor.execute(query, (thirty_days_ago,))
    data = cursor.fetchall()

    # Create a list of dictionaries
    data_list = [{"Chain": row[0], "TVL": row[1]} for row in data]

    # Display the data
    for entry in data_list:
        print(f"Chain: {entry['Chain']}, TVL: ${entry['TVL']:.2f}")

    # Close the database connection
    db_connection.close()





def main():
    # Fetch and store data
    #fetch_and_store_chain_data()
    
    # Query and process the data
    process_and_display_data()

if __name__ == "__main__":
    main()
