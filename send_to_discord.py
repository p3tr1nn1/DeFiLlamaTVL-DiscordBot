import json
import requests
import os

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def send_discord_message(webhook_url, embeds):
    data = {"embeds": embeds}
    response = requests.post(webhook_url, json=data)
    return response.status_code

def create_embed(result):
    # Create an embed for better formatting
    return {
        "title": f"{result['chain']} TVL Analysis",
        "description": result['message'],
        "color": 5814783,  # You can change the color
        "fields": [
            {"name": "Current TVL", "value": f"**{result['current_tvl']}**", "inline": False}
        ]
    }

def main():
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Discord webhook URL not found in environment variables.")
        return

    analysis_results = read_json_file('tvl_analysis_results.json')
    
    # Reverse the list to send messages from lower to higher TVL
    analysis_results.reverse()

    # Prepare and send messages as embeds
    embeds = []
    for result in analysis_results:
        embed = create_embed(result)
        embeds.append(embed)
        # Discord limits a maximum of 10 embeds per message
        if len(embeds) == 10:
            send_discord_message(webhook_url, embeds)
            embeds = []

    # Send any remaining embeds
    if embeds:
        send_discord_message(webhook_url, embeds)

if __name__ == "__main__":
    main()
