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
    return {
        "title": protocol["name"],
        "description": f"TVL: {protocol['tvl']}\nChange (1h): {protocol['change_1h']}\nChange (1d): {protocol['change_1d']}\nChange (7d): {protocol['change_7d']}\nDescription: {protocol['description']}\nURL: {protocol['url']}",
        "color": 5814783,  # You can change the color
        "image": {
            "url": protocol["logo"]
        }
    }

def main():
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    protocol_data = read_json_file('top_10_protocols.json')
    
    embeds = [create_embed(protocol) for protocol in protocol_data["protocols"]]

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
