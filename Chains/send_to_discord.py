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
    return {
        "title": f"{result['chain']} TVL Analysis",
        "description": f"**30-Day TVL Increase: {result['increase_30d']:.2f}%**",
        "color": 5814783,  # You can change the color
        "fields": [
            {"name": "Current TVL", "value": f"{result['current_tvl']}", "inline": False}
            
        ]
    }

def create_banner_embed():
    return {
        "title": "Top 10 Protocols with Highest TVL Percentage Change",
        "description": "Displaying top 10 protocols with highest TVL percentage change in the last 30 days, with a total TVL higher than 10 million USD.",
        "color": 16711680  # You can change the color of the banner
    }


def main():
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Discord webhook URL not found in environment variables.")
        return

    analysis_results = read_json_file('tvl_analysis_results.json')
    
    # Get the first 10 analysis results
    first_10_results = analysis_results[:10]

    # Create a banner embed
    banner_embed = create_banner_embed()

    # Prepare and send messages as embeds
    embeds_banner = [banner_embed]  # Add the banner embed first
    send_discord_message(webhook_url, embeds_banner)

    embeds = []
    for result in first_10_results:
        embed = create_embed(result)
        embeds.append(embed)

    # Send the embeds as a single Discord message
    if embeds:
        send_discord_message(webhook_url, embeds)

if __name__ == "__main__":
    main()
