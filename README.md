# DeFi Llama Discord TVL Analysis

This repository contains a collection of Python scripts for analyzing and monitoring the Total Value Locked (TVL) of various decentralized finance (DeFi) chains using the DeFi Llama API. The scripts provide insights into TVL changes over different time periods and can send notifications to a Discord channel.

## Features

- **Data Fetching**: Retrieve blockchain TVL data from the DeFiLlama API.
- **Data Storage**: Store and manage data in an SQLite database.
- **Data Analysis**: Analyze TVL data to identify significant trends.
- **Discord Integration**: Report analysis results on Discord using rich embeds.

## Installation

Before using the scripts, ensure you have Python 3 and pip3 installed. If not, you can install them as follows:

```bash
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
```

2. **Install Required Libraries**:
   You need Python 3.x installed. Then, install the required libraries using:
   ```
   pip install requests sqlite3 json
   ```


## Usage
To run the analysis and monitoring scripts, follow these steps:

Set up the Discord Webhook:

Create a Discord webhook for receiving notifications in your channel.

Export the webhook URL as an environment variable in your Linux terminal:

```bash
export DISCORD_WEBHOOK_URL="your_discord_webhook_url_here"
```

## Run the Scripts:
Execute the run_scripts.py script using Python 3:
```bash
python3 run_scripts.py
```

This script will run the following in order:
```
defillama_chain_data_sync.py: Syncs DeFi chain data and stores it in the defillama_data.db database.

historical_tvl_storage.py: Fetches historical TVL data for chains with TVL greater than 5 million and stores it in the defillama_historical.db database.

defillama_tvl_analysis.py: Analyzes TVL data, calculates percentage changes, and generates JSON analysis results in the tvl_analysis_results.json file.

send_to_discord.py: Sends TVL analysis results as Discord messages to your specified channel.
```

The scripts provide insights into TVL changes over different time periods and can help you stay informed about the DeFi market.

## Discord Webhook
To set up the Discord webhook, follow these steps:

```
Open your Discord server and channel where you want to receive notifications.

Click on "Edit Channel" -> "Integrations" -> "Webhooks" -> "Create Webhook."

Customize the webhook name, profile picture, and channel (if needed), and click "Save."
```

Copy the webhook URL generated for your channel.
In your Linux terminal, export the webhook URL as an environment variable:

```bash
export DISCORD_WEBHOOK_URL="your_discord_webhook_url_here"
```

Now, the scripts will use this webhook URL to send notifications to your Discord channel.



![DeFi Llama Logo](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXPMIS5tfUOecqePdv2nLuztb2gNJnTghuk3vw7A0QHMy20WV35HsMM3eaOzp1xxjPy_E&usqp=CAU)
![Discord Logo](https://cdn.iconscout.com/icon/free/png-256/free-discord-4408564-3649907.png?f=webp)
![Python Logo](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0bbtxptgGMNHCpEo7uh_5bCtd4APV4lZzoypojrHB1es3UroxBzc1wqUESDr9mMaCGtE&usqp=CAU)
