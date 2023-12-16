import sqlite3

# Initialize and connect to SQLite database for protocol data
def init_protocol_db():
    conn = sqlite3.connect('protocol_data.db')
    print("Connected to the database.")
    return conn

# Query all TVL data for all IDs along with names
def query_all_tvl_and_name(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT name, tvl FROM protocols')
    return cursor.fetchall()

# Calculate the average TVL from the queried data
def calculate_average_tvl(data):
    total_tvl = sum(entry[1] for entry in data)
    num_entries = len(data)
    print(total_tvl/num_entries)
    return total_tvl / num_entries if num_entries > 0 else 0

# Create a new table for protocols with TVL >= 70% of the average TVL
def create_high_tvl_table(conn, average_tvl):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_tvl_protocols (
            name TEXT PRIMARY KEY,
            tvl REAL
        )
    ''')
    conn.commit()
    print("High TVL protocols table created.")

# Insert protocols with TVL >= 70% of the average TVL into the new table
def insert_high_tvl_protocols(conn, data, average_tvl):
    cursor = conn.cursor()
    # Clear existing records in the high_tvl_protocols table
    cursor.execute("DELETE FROM high_tvl_protocols")
    conn.commit()

    for entry in data:
        if entry[1] >= average_tvl * 0.7:
            cursor.execute('''
                INSERT OR REPLACE INTO high_tvl_protocols (
                    name, tvl
                ) VALUES (?, ?)
            ''', (
                entry[0], entry[1]
            ))
            conn.commit()
            print(f"Inserted data for protocol: {entry[0]}, TVL: {entry[1]}")

def main():
    conn = init_protocol_db()
    all_tvl_data = query_all_tvl_and_name(conn)
    average_tvl = calculate_average_tvl(all_tvl_data)
    create_high_tvl_table(conn, average_tvl)
    insert_high_tvl_protocols(conn, all_tvl_data, average_tvl)
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
