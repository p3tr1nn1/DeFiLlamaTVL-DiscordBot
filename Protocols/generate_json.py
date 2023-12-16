import sqlite3
import json

# Initialize and connect to SQLite database for protocol data
def init_protocol_db():
    conn = sqlite3.connect('protocol_data.db')
    print("Connected to the database.")
    return conn

# Query the top 10 protocols with the highest TVL from high_tvl_protocols
def query_top_10_high_tvl_protocols(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name FROM high_tvl_protocols
        ORDER BY tvl DESC
        LIMIT 15
    ''')
    return cursor.fetchall()

# Query additional information for a protocol by name
def query_protocol_info_by_name(conn, protocol_name):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, tvl, mcap, change_1h, change_1d, change_7d, description, url, logo
        FROM protocols
        WHERE name = ?
    ''', (protocol_name,))
    return cursor.fetchone()

def create_json_data(top_protocols, conn):
    data = {
        "protocols": []
    }
    
    for protocol_name in top_protocols:
        protocol_info = query_protocol_info_by_name(conn, protocol_name[0])

        if protocol_info:
            name, tvl, mcap, change_1h, change_1d, change_7d, description, url, logo = protocol_info
            
            # Skip protocol if mcap is None
            if mcap is None:
                continue
            
            # Format TVL with commas and two decimal places
            formatted_tvl = "{:,.2f}".format(tvl)
            
            # Format mcap with commas, two decimal places, and 'M' symbol
            formatted_mcap = "{:,.2f}M".format(mcap / 1_000_000)
            
            # Format change_1h, change_1d, and change_7d with two decimal places and a '%'
            formatted_change_1h = "{:.2f}%".format(change_1h)
            formatted_change_1d = "{:.2f}%".format(change_1d)
            formatted_change_7d = "{:.2f}%".format(change_7d)
            
            protocol_data = {
                "name": name,
                "tvl": formatted_tvl,
                "mcap": formatted_mcap,
                "change_1h": formatted_change_1h,
                "change_1d": formatted_change_1d,
                "change_7d": formatted_change_7d,
                "description": description,
                "url": url,
                "logo": logo
            }
            
            # Filter out keys with None (null) values
            protocol_data = {k: v for k, v in protocol_data.items() if v is not None}
            data["protocols"].append(protocol_data)
    
    return data






# Save JSON data to a file (overwrite if exists)
def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    conn = init_protocol_db()
    top_10_protocols = query_top_10_high_tvl_protocols(conn)

    if top_10_protocols:
        data = create_json_data(top_10_protocols, conn)
        conn.close()  # Close the database connection after fetching data

        json_filename = 'top_10_protocols.json'
        save_json_to_file(data, json_filename)

        # Print the JSON data
        print(json.dumps(data, indent=4))
    else:
        print("No data to generate JSON.")

if __name__ == "__main__":
    main()
