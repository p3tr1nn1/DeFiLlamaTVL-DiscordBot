import json
import requests
import os

# Function to send a Discord message with embeds
def send_discord_message(webhook_url, data):
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    return response.status_code

# Read the JSON file with protocol data
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Create an embed for a protocol
def create_embed(protocol):
    changes =f"Change (1h): {protocol['change_1h']}\n" \
                     f"Change (1d): {protocol['change_1d']}\n" \
                     f"Change (7d): {protocol['change_7d']}"
    
    return {
        "title": protocol["name"],        
        "fields": [
            {
                "name": "TVL",                
                "value": protocol["tvl"],                
                "inline": False
            },
            {
                "name": "Marketcap",
                "value": protocol["mcap"],
                "inline": False
            },
             {
                "name": "Changes",
                "value": changes,                
                "inline": False
            },
            {
                "name": "Description",
                "value": protocol["description"],
                "inline": True
            },
            {
                "name": "URL",
                "value": protocol["url"],
                "inline": False
            }
        ],
        "color": 5814783,  # You can change the color
        "image": {
            "url": protocol["logo"]
        }
    }

def create_banner_embed():
    return {
        "title": "Top 10 Protocols with Highest TVL",
        "description": "***Displaying top 10 protocols with highest TVL.***",
        "color": 16711680  # You can change the color of the banner
    }

def main():
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Discord webhook URL not found in environment variables.")
        return

    protocol_data = read_json_file('top_10_protocols.json')
    
    # Create the banner embed
    banner_embed = create_banner_embed()
    
    # Create individual protocol embeds
    embeds = [banner_embed]  # Add the banner embed first
    embeds.extend([create_embed(protocol) for protocol in protocol_data["protocols"]])

    if embeds:
        data = {
            "embeds": embeds
        }

        response_status = send_discord_message(webhook_url, data)

        if response_status == 204:
            print("Discord message sent successfully.")
        else:
            print(f"Failed to send Discord message. Status code: {response_status}")
    else:
        print("No data to send to Discord.")


if __name__ == "__main__":
    main()
