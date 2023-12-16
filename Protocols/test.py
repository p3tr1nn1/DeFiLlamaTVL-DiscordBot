import sqlite3
import json

# Initialize and connect to SQLite database for protocol data
def init_protocol_db():
    conn = sqlite3.connect('protocol_data.db')
    print("Connected to the database.")
    return conn

# Calculate the average TVL from the queried data
def calculate_average_tvl(data):
    total_tvl = sum(entry[0] for entry in data)
    num_entries = len(data)
    return total_tvl / num_entries if num_entries > 0 else 0

# Query protocols with at least 70% of the average TVL
def query_high_tvl_protocols(conn, average_tvl):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, symbol, description, chain, logo, 
               change_1h, change_1d, change_7d, tvl, mcap
        FROM protocols
        WHERE tvl >= ?
    ''', (average_tvl * 0.7,))
    return cursor.fetchall()

# Save protocol data to a JSON file
def save_to_json(data):
    with open('high_tvl_protocols.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    conn = init_protocol_db()
    cursor = conn.cursor()
    cursor.execute('SELECT tvl FROM protocols')
    tvl_data = cursor.fetchall()
    average_tvl_data = calculate_average_tvl(tvl_data)
    high_tvl_protocols = query_high_tvl_protocols(conn, average_tvl_data)
    conn.close()

    if high_tvl_protocols:
        save_to_json(high_tvl_protocols)
        print("High TVL protocols saved to high_tvl_protocols.json:")
        for protocol in high_tvl_protocols:
            print(f"Name: {protocol[1]}, TVL: {protocol[9]}")

if __name__ == "__main__":
    main()
