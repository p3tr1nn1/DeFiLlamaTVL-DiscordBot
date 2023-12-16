import sqlite3

# Initialize and connect to SQLite database for protocol data
def init_protocol_db():
    conn = sqlite3.connect('protocol_data.db')
    print("Connected to the database.")
    return conn

# Query all TVL data for all IDs
def query_all_tvl(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, tvl FROM protocols')
    return cursor.fetchall()

# Calculate the average TVL from the queried data
def calculate_average_tvl(data):
    total_tvl = sum(entry[1] for entry in data)
    num_entries = len(data)

    return total_tvl / num_entries if num_entries > 0 else 0

# Format TVL amount in human-readable format
def format_tvl(tvl):
    if tvl < 1_000_000:
        return f"${tvl:.2f}"
    elif tvl < 1_000_000_000:
        return f"${tvl / 1_000_000:.2f} million"
    else:
        return f"${tvl / 1_000_000_000:.2f} billion"

def main():
    conn = init_protocol_db()
    all_tvl_data = query_all_tvl(conn)
    average_tvl = calculate_average_tvl(all_tvl_data)
    formatted_average_tvl = format_tvl(average_tvl)
    
    print(f"The average Total Value Locked (TVL) across all protocols is {formatted_average_tvl}.")

if __name__ == "__main__":
    main()
